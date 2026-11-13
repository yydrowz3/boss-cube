from pathlib import Path
import json, zipfile, shutil, re, xml.etree.ElementTree as E
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'models' / 'BOSS_cube_35mm'
NS = {'c': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

with zipfile.ZipFile(OUT/'BOSS_cube_35mm_P2S_04.3mf') as z:
    root = E.fromstring(z.read('3D/3dmodel.model'))
    sub = E.fromstring(z.read('3D/Objects/object_1.model'))
    config = json.loads(z.read('Metadata/project_settings.config'))
    meshes = []
    for comp in root.findall('.//c:component', NS):
        obj = sub.find('.//c:object[@id="'+comp.get('objectid')+'"]', NS)
        vs = [[float(a.get(k)) for k in ('x','y','z')] for a in obj.findall('.//c:vertex', NS)]
        fs = [[int(a.get(k)) for k in ('v1','v2','v3')] for a in obj.findall('.//c:triangle', NS)]
        m = trimesh.Trimesh(vs, fs, process=True)
        m.apply_translation(list(map(float, comp.get('transform').split()))[9:12])
        meshes.append(m)
body, letters = meshes
assert all(m.is_watertight and m.is_winding_consistent and m.volume > 0 for m in meshes)
assert np.allclose(body.extents, [35,35,35])
assert np.allclose(letters.extents[[0,2]], [28,.8])
assert np.isclose(body.bounds[1,2], letters.bounds[0,2])
assert np.allclose(trimesh.util.concatenate(meshes).extents, [35,35,35.8])
pieces = letters.split()
assert len(pieces) == 8
assert sum(1-p.euler_number/2 for p in pieces) == 14
assert np.all(letters.bounds[0,:2] > body.bounds[0,:2]) and np.all(letters.bounds[1,:2] < body.bounds[1,:2])
expected = dict(printer_settings_id='Bambu Lab P2S 0.4 nozzle', print_settings_id='0.20mm Standard @BBL P2S',
    layer_height='0.2',initial_layer_print_height='0.2',wall_loops='2',sparse_infill_density='10%',
    sparse_infill_pattern='gyroid',top_shell_layers='5',bottom_shell_layers='3',
    enable_support='0',ironing_type='no ironing',enable_prime_tower='1')
for k,v in expected.items(): assert config[k] == v, (k,config[k])
assert 'sparse_infill_pattern' in config['different_settings_to_system'][0]
write_json(OUT/'project_validation.json', dict(overall_mm=[35,35,35.8], body_mm=[35,35,35],
    lettering_width_mm=28, relief_mm=.8, watertight=True, winding_consistent=True,
    lettering_connected_components=8, lettering_holes=14, contact_z_mm=35,
    lettering_supported_by_body=True, configured_process_verified=True,
    actual_AMS_slots_verified=False, physical_print_test_performed=False))

stats = {}
for side in (35,50):
    data=json.loads((ROOT/'archive'/'qa'/f'result{side}.json').read_text())['sliced_plates'][0]
    with zipfile.ZipFile(ROOT/'archive'/'qa'/f'comparison{side}_sliced.3mf') as z:
        code=z.read('Metadata/plate_1.gcode').decode()
        header=code.splitlines()[:100]
        assert '; filament: 2,3' in header
        layer_info=z.read('Metadata/slice_info.config').decode()
        if side == 35:
            assert 'layer_ranges="0 174"' in layer_info and 'layer_ranges="175 178"' in layer_info
        times=next(x for x in header if x.startswith('; model printing time:'))
    assert data['filament_change_times'] == 1
    stats[str(side)] = dict(total_estimated_seconds=data['total_predication'],
        gcode_time_header=times, gui_total_time=('38m37s' if side==35 else '1h5m'),
        prepare_time='7m2s',model_time=('31m35s' if side==35 else '57m53s'),
        total_g=sum(f['total_used_g'] for f in data['filaments']),
        model_g=sum(f['main_used_g'] for f in data['filaments']),
        cyan_g=data['filaments'][0]['total_used_g'],white_g=data['filaments'][1]['total_used_g'],
        flush_g=.59,tower_g=(5.12 if side==35 else 7.14),
        filament_changes=1,used_project_filaments=[2,3],layer_count=(179 if side==35 else 254),
        warning=data['warning_message'])
stats['estimated_time_reduction_percent']=100*(1-stats['35']['total_estimated_seconds']/stats['50']['total_estimated_seconds'])
stats['estimated_material_reduction_percent']=100*(1-stats['35']['total_g']/stats['50']['total_g'])
stats['conditions']='P2S 0.4 mm; 0.20 mm Standard; 10% gyroid; existing Bambu PLA Matte presets. Actual rolls and AMS slots not yet verified. Software estimates, not a physical print test.'
write_json(OUT/'slice_comparison.json',stats)

source=OUT/'source';source.mkdir(exist_ok=True)
shutil.copy2(ROOT/'scripts'/'build_model_35mm.py',source/'build_model.py')
shutil.copy2(ROOT/'assets'/'reference'/'images.jpg',source/'images.jpg')
write_json(source/'verified_process_settings.json',expected | {'curr_bed_type':config['curr_bed_type'],
    'project_filament_2':'Bambu PLA Matte, cyan #53CAC6; actual roll unverified',
    'project_filament_3':'Bambu PLA Matte, white #FFFFFF; actual roll unverified'})
(source/'README.md').write_text('''# 源码使用

[English](README.en.md) | 简体中文

`build_model.py` 从旁边的 `images.jpg` 提取原图字形，重新生成通用彩色 3MF、两份 STL、轮廓数据、几何验证和预览图。

安装 Python 3.11 或更新版本与 uv 后，在此目录运行：

```sh
uv run build_model.py
```

脚本头部声明了依赖，uv 会建立运行环境。输出在本目录新建的 `BOSS_cube_35mm` 子目录，不会覆盖交付的 Bambu 工程。

尺寸常量为 `SIDE=35.0`、`LOGO_WIDTH=28.0`、`RELIEF=0.8`，单位毫米。字形直接来自参考图，没有替换字体。

生成器输出不绑定机型。实际 P2S 工艺已保存在交付目录的 `BOSS_cube_35mm_P2S_04.3mf`；`verified_process_settings.json` 是本次核对的参数清单，可按主说明书在 Studio 中复现。AMS 槽位需连接后确认。
''',encoding='utf-8')
comparison=OUT/'comparison';comparison.mkdir(exist_ok=True)
shutil.copy2(ROOT/'archive'/'qa'/'BOSS_cube_50mm_comparison.3mf',comparison/'BOSS_cube_50mm_P2S_04_comparison.3mf')
print(json.dumps(stats,ensure_ascii=False,indent=2))
