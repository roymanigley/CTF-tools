FROM ubuntu:22.04
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y && apt-get install \
    build-essential \
    binwalk \
    curl \
    dirb \
    dnsutils \
    ftp \
    gdb \
    gcc \
    git \
    gobuster \
    hashcat \
    hydra \
    language-pack-en \
    libbz2-dev \ 
    libgmp-dev \
    libpcap-dev \
    libssl-dev \
    netcat \
    net-tools \
    nikto \
    nmap \
    openssh-server \
    openvpn \
    pkg-config \
    python3-virtualenv \
    pip \
    ruby \
    ruby-dev \
    smbclient \
    sqlmap \
    sudo \
    tcpdump \
    unzip \
    vim \
    vim-addon-manager \
    wget \
    yasm \
    zlib1g-dev \
    zsh \
    zsh-autosuggestions \
    zsh-syntax-highlighting \
    python3.10-venv -y

# RUN git clone https://github.com/3ndG4me/KaliLists /usr/share/wordlists
# RUN git clone https://gitlab.com/kalilinux/packages/webshells /usr/share/webshells
# RUN git clone https://gitlab.com/exploit-database/exploitdb.git /usr/share/exploit-database
# RUN ln -s /usr/share/exploit-database/searchsploit /usr/sbin/searchsploit
RUN git clone https://github.com/openwall/john -b bleeding-jumbo /usr/src/john
RUN cd /usr/src/john/src && ./configure && make -s clean && make -sj4
RUN git clone https://github.com/CiscoCXSecurity/enum4linux /usr/share/enum4linux
RUN sed -i 's#which $prog 2>&1#which $prog 2>/dev/null#g' /usr/share/enum4linux/enum4linux.pl
RUN gem install wpscan
RUN wget https://apt.metasploit.com/pool/main/m/metasploit-framework/metasploit-framework_6.4.14~20240616102556~1rapid7-1_amd64.deb -O /tmp/metasploit-framework_6.3.6.deb
RUN dpkg -i /tmp/metasploit-framework_6.3.6.deb


RUN update-locale
RUN useradd -rm -d /home/hacker -G sudo -u 1001 hacker
RUN echo 'hacker:hacker' | chpasswd
USER hacker
RUN mkdir /home/hacker/share
RUN wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -O /home/hacker/share/linpeas.sh
WORKDIR /home/hacker
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && sed -i 's/\(ZSH_THEME=\).\+/\1"agnoster"/g' ~/.zshrc
RUN echo "source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc
RUN echo "source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc

RUN echo "set nu" > ~/.vimrc
RUN echo "syntax on" > ~/.vimrc
RUN echo "filetype plugin indent on" >> ~/.vimrc
RUN echo "set tabstop=4" >> ~/.vimrc
RUN echo "set shiftwidth=4" >> ~/.vimrc
RUN echo "set expandtab" >> ~/.vimrc
RUN echo "nnoremap <C-s> :w<CR>" >> ~/.vimrc
RUN echo "inoremap <C-s> <ESC>:w<CR>a" >> ~/.vimrc
RUN echo "nnoremap <C-q> :qa<CR>" >> ~/.vimrc
RUN echo "inoremap <C-q> <ESC>:qa<CR>" >> ~/.vimrc
RUN echo "nnoremap <C-d> :q<CR>" >> ~/.vimrc
RUN echo "inoremap <C-d> <ESC>:q<CR>" >> ~/.vimrc

CMD tail -f /dev/null
