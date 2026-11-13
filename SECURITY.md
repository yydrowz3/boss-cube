# Security Policy

## Supported versions

Security reports are accepted for the latest code on `main`. This repository currently has no tagged releases or maintained release branches.

| Version or artifact | Security maintenance |
| --- | --- |
| Latest `main` | Reports accepted; fixes are made on a best-effort basis |
| Older commits, historical ZIP packages, and archived snapshots | No backport commitment; reproduce against the latest applicable code where possible |

## Report a vulnerability privately

Email [yydrowz3@gmail.com](mailto:yydrowz3@gmail.com) with the subject `Security report: boss-cube`.

Please include:

- The affected commit, script, dependency, or artifact.
- A description of the vulnerability, its impact, and any required conditions.
- Minimal reproduction steps and a small proof of concept or sample input, if available.
- Relevant operating system, Python, dependency, and Bambu Studio versions.
- Your preferred contact method and whether you would like public credit.

Remove credentials, personal information, printer identifiers, and private network details from examples and logs. Describe sensitive evidence in the initial message and coordinate how to share it. Do not publish exploit details, sensitive samples, or a public fix that exposes the issue before coordinating disclosure.

This email address is the reporting channel regardless of whether GitHub's private vulnerability reporting feature is enabled.

## Scope

Relevant reports include vulnerabilities in the repository's scripts and workflows that could lead to unintended file access, file modification, code execution, or disclosure of private data. Include dependency vulnerabilities when you can explain how the project's usage is affected.

Ordinary model defects, print quality problems, inaccurate time estimates, documentation errors, and feature requests belong in [Issues](https://github.com/yydrowz3/boss-cube/issues). For a vulnerability in Bambu Studio, printer firmware, or another independently maintained dependency, use that upstream project's security reporting process. If this repository also needs a change, report that impact here privately.

## Handling and coordinated disclosure

The maintainer will review reports, seek clarification when needed, and work with the reporter to assess impact and prepare an appropriate fix or mitigation. Response and resolution depend on availability and complexity; there is no guaranteed response or remediation deadline.

Disclosure timing and credit will be coordinated with the reporter, and with upstream maintainers when relevant. Reports will be handled privately during investigation, with information shared only as needed to investigate and resolve the issue. The maintainer will communicate the outcome and any available mitigation through the agreed reporting channel.

Security reporting does not require sending a print job or accessing anyone else's printer, account, device, or data. Keep reproduction within environments and materials you are authorized to use.
