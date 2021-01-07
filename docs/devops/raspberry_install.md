# Raspberry Pi Servers

The basis building blocks of the Robomind Academy infrastructure are 
Raspberry Pi 4 nodes running Ubuntu Server software.

# Install primary server with USB disk

The first Raspberry Pi 4/4Gb will be the master system. It will boot from a USB SSD disk and run the following software:

* Ubuntu Server for Raspberry Pi 20.10
* PostgreSQL
* RabbitMQ server
* logging and monitoring software

Getting the Raspberry Pi to boot from  USB disk (and not from micro SD card) is done account to
[this page](https://www.instructables.com/Raspberry-Pi-4-USB-Boot-No-SD-Card/).

After installing the OS, updating and booting correctly  you will need to the following extra steps.

* update DHCP server so a fixed IP address is assigned
* create a new account and put it in sudo group
* add SSH credentials

```bash
sudo addgroup jan
sudo adduser --gid 1001 jan
sudo usermod -aG sudo jan
```

# Install slave nodes

The other three Raspberry Pi 4/8Gb will be slave nodes. They will boot from SD card. 
Install the following software:

* Ubuntu Server for Raspberry Pi 20.10
## References

