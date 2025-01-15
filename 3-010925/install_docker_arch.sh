sudo pacman -Sy

sudo pacman -S --needed ca-certificates curl

sudo pacman -S docker
sudo pacman -S docker-compose

sudo systemctl start docker
sudo systemctl enable docker

sudo systemctl status docker
