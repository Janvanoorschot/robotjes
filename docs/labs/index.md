# Setup Labs.robomindacademy.com

## Layout

The Robomind Academy development environment 'labs.robomindacadem.com' consists of a
headend server with a stack of Raspberry Pi 4's behind it. The headend server runs:

* Ubuntu server
* Docker
* Postgresql SQL server (iron)
* RabbitMQ messaging server (iron)
* The RMG robomind academy Grails software (container)

The stack of Raspberry Pi 4's behind it run:

* Ubuntu server
* Docker swarm
* robomnind/robo container
* robomind/robotjes container

## Content

* [Raspberry 4 servers](raspberry_install)
* [labs_install](labs_install)


