# RSVdb: A comprehensive database of *in vivo* mRNA structures

![figure1](./1.png)

RSVdb focuses on the research and experimental data related to the mRNA structure in vivo. It includes all the studies of the in vivo mRNA structure labeled by DMS reagent since the first proposed DMS-profiling method in 2014 (Rouskin et al. 2014; Ding et al. 2014). Our database including 622,429 RNAs from 178 samples of 10 studies in 8 species, displays the statistical presentation of mapping data, even predict and visualize mRNA structure in silico and in vivo. The project is supported by the National Natural Science Foundation of China (Grant 31771474). Servers and network services are provided by the Network & Education Technology Center of NWAFU.

Main site please visit https://taolab.nwsuaf.edu.cn/rsvdb/

The repository contains the source code for the front and back ends of RSVdb. The structure of the website is: 

![figure2](./2.png)


## Installation

You need to install the following software:
>* Python 3.7
>* pipenv
>* RNAstructure (Linux Text Command Version)

Once you have these conditions, download the entire file and execute the following command.

>1. cd RSVdb
>2. pipenv install
>3. pipenv shell
>4. flask run

You can then visit RSVdb via http://127.0.0.1:5000/.

The repository contains the main functions of RSVdb, including data browsing and structure prediction. If you need to use 'viewer' functionality, please install RNAstructure (http://rna.urmc.rochester.edu/RNAstructure.html), where structural prediction relies heavily on Fold software.

