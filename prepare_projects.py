"""Derive two identically configured Bambu projects from a saved local project.
Preserves the existing printer profile and filament presets; never sends a job.
"""
from pathlib import Path
import json, zipfile, xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parent
SEED=ROOT/'_qa'/'original50_session.3mf'
OUT=ROOT/'BOSS_cube_35mm'
C='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
P='http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
E.register_namespace('',C);E.register_namespace('p',P)
E.register_namespace('BambuStudio','http://schemas.bambulab.com/package/2021')

def xml(x): return E.tostring(x,encoding='utf-8',xml_declaration=True)

def build(side,dest):
    with zipfile.ZipFile(SEED) as z: files={n:z.read(n) for n in z.namelist()}
    config=json.loads(files['Metadata/project_settings.config'])
    config.update(layer_height='0.2',initial_layer_print_height='0.2',wall_loops='2',
                  sparse_infill_density='10%',sparse_infill_pattern='gyroid',
                  top_shell_layers='5',bottom_shell_layers='3',enable_support='0',
                  ironing_type='no ironing',enable_prime_tower='1')
    # Studio only reapplies differences recorded here when resolving presets.
    changes=config.get('different_settings_to_system',['','','','',''])
    keys=set(filter(None,changes[0].split(';')))
    keys.update(['sparse_infill_density','sparse_infill_pattern'])
    changes[0]=';'.join(sorted(keys))
    config['different_settings_to_system']=changes
    assert config['printer_settings_id']=='Bambu Lab P2S 0.4 nozzle'
    assert config['print_settings_id']=='0.20mm Standard @BBL P2S'
    files['Metadata/project_settings.config']=json.dumps(config,indent=2,ensure_ascii=False).encode()
    model=E.fromstring(files['3D/3dmodel.model'])
    for m in list(model.findall(f'{{{C}}}metadata')):
        if m.get('name') in ['DesignerUserId','Designer','DesignerCover']:
            model.remove(m)
        elif m.get('name')=='Title':m.text=f'BOSS cube {side}mm'
        elif m.get('name')=='Description':m.text=f'{side}mm cyan cube, 0.8mm white raised lettering. P2S 0.4mm, 0.20mm layers, 10% gyroid. Verify AMS mapping before printing.'
    for comp in model.findall(f'.//{{{C}}}component'):
        t=comp.get('transform').split();t[11]=str(side/2 if comp.get('objectid')=='1' else side+0.4)
        comp.set('transform',' '.join(t))
    files['3D/3dmodel.model']=xml(model)
    mesh=E.fromstring(files['3D/Objects/object_1.model'])
    for obj in mesh.findall(f'.//{{{C}}}object'):
        for v in obj.findall(f'.//{{{C}}}vertex'):
            for axis in ('x','y'):v.set(axis,f'{float(v.get(axis))*side/50:.9f}')
            if obj.get('id')=='1':v.set('z',f'{float(v.get("z"))*side/50:.9f}')
            else:v.set('z','0.4' if float(v.get('z'))>0 else '-0.4')
    files['3D/Objects/object_1.model']=xml(mesh)
    settings=E.fromstring(files['Metadata/model_settings.config'])
    obj=settings.find('object')
    for m in obj.findall('metadata'):
        if m.get('key')=='name':m.set('value',f'BOSS cube {side}mm')
        if m.get('key')=='extruder':m.set('value','2')
    for part in obj.findall('part'):
        z=side/2 if part.get('id')=='1' else side+0.4
        for m in part.findall('metadata'):
            key=m.get('key')
            if key=='matrix':
                a=m.get('value').split();a[11]=str(z);m.set('value',' '.join(a))
            elif key=='source_offset_z':m.set('value',str(z))
            elif key=='source_file':m.set('value',f'BOSS_cube_{side}mm.3mf')
    for a in settings.findall('.//assemble_item'):
        if a.get('volume_id') is not None:
            t=a.get('transform').split();t[11]=str(side/2 if a.get('volume_id')=='0' else side+0.4);a.set('transform',' '.join(t))
    for plate in settings.findall('plate'):
        for m in list(plate.findall('metadata')):
            if m.get('key') in ('thumbnail_file','thumbnail_no_light_file','top_file','pick_file'):plate.remove(m)
    files['Metadata/model_settings.config']=xml(settings)
    # These caches describe the previous model. Studio regenerates them on save.
    keep={n:data for n,data in files.items() if not (n.endswith('.png') or n in ['Metadata/plate_1.json','Metadata/slice_info.config','Metadata/filament_sequence.json'])}
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in keep.items():z.writestr(n,data)
    print(dest)

if __name__=='__main__':
    build(35,OUT/'BOSS_cube_35mm_P2S_04.3mf')
    build(50,ROOT/'_qa'/'BOSS_cube_50mm_comparison.3mf')
