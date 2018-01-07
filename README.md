Tested for Linux 17.10 with 6 nvidia 1070 graphics cards.
No AMD support for the moment.

Install nvidia drivers manually (tested with nvidia-384)

For ASRock B250 Fatality gaming k4 motherboard:
- Top of Lower Usable RAM (TOLUD) -> set to highest (3.5GB)
- pcie: auto
- grub: acpi=off (bug somewhere in Linux/Ubuntu). This may cause soft reboot/shutdown to get stuck...

Deploy:
```
ansible-playbook -i production --ask-pass --ask-become-pass -u miner site.yml
```
