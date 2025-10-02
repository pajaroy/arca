# Comandos Utiles




## Crear modulo base :

```bash
mkdir -p test/project/{src,docs,archive,config,meta,templates}
```



# Comandos para iniciar docker

# Construir docker: 

docker build -t [proyecto] .

# Modo persistente : 

sudo docker run -it -v $(pwd):/[app] --name [proyecto] [imagen] bash

# listar dockers: 

docker ps -a

# reutilizar docker: 

sudo docker start -ai [proyecto]

# Modo laboratorio: 

sudo docker run -it --rm arca bash

docker run --name arca-dev-test -it --rm arca-dev bash