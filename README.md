# ViResA-mimo #

## Prerequisites (for real-data workloads) ##
Server Side:
- Install Xen Hypervisor on each physical machine (web server, database server)
- Create DomUs-VMs to host the server applications (Apache, MySQL)
- Set the domain names and IP addresses of the DomUs in server_consolidation.py
- Setup a physical machine (remote server) and create ssh connections with the other server physical machines (web server, database server)
- Copy viresa folder to the root directory of Dom0 on each physical machine (VM1, VM2) and to the remote server

Client Side:
- Copy  RUBiS (Client-Side) folder to the root directory
- Install screen

## Description ##
The ViResA (Virtualized [server] Resource Allocation) project studies the performance of various methods for state estimation of the usage and allocation in virtualized servers. Resource Allocation can be predicted using synthetic workloads, or real-data workloads via RUBiS auction site application.

## How do I get set up? ##
- VM1 - Web Server tier:
  - Install Apache2
  - Copy RUBiS/PHP folder to /var/www/html/
  - Change Database Server IP address in the file PHPprinter.php

- VM2 - Database Server tier:
  - Install MySQL
  - Create user for MySQL
  - Create and populate database (see RUBiS/setup/db/README for more info)

- Client tier:
  - Copy RUBiS folder to the root directory
  - Configure IP addresses, workload scenarios in /RUBiS/Client/rubis.properties
  - Copy initialize.sh to the root directory

- Login to the remote server, go to the viresa directory and run server_consolidation.py in terminal

## Publication ##
If our work helps your works in an academic/research context, please cite the following publications:

@inproceedings{makridis2017dynamic,
  title={Dynamic CPU resource provisioning in virtualized servers using maximum correntropy criterion Kalman filters},
  author={Makridis, Evagoras and Deliparaschos, Kyriakos M and Kalyvianaki, Evangelia and Charalambous, Themistoklis},
  booktitle={2017 22nd IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)},
  pages={1--8},
  year={2017},
  organization={IEEE}
}
@article{makridis2018robust,
  title={Robust Dynamic CPU Resource Provisioning in Virtualized Servers},
  author={Makridis, Evagoras and Deliparaschos, Kyriakos and Kalyvianaki, Evangelia and Zolotas, Argyrios and Charalambous, Themistoklis},
  journal={arXiv preprint arXiv:1811.05533},
  year={2018}
}

## Who do I talk to? ##
* Dr. Kyriakos Deliparaschos: k.deliparaschos@cut.ac.cy
* Dr. Themistoklis Charalambous: themistos@gmail.com
* Evagoras Makridis: evagoras.makridis@gmail.com
