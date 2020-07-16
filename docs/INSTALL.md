**Table of Contents**

1. [Requirements](#requirements)
2. [Install Dependencies](#install-dependencies)
   * [Ubuntu 14.04 / Debian 8](#ubuntu-1404--debian-8)
   * [Ubuntu 16.04](#ubuntu-1604)
   * [Ubuntu 18.04](#ubuntu-1804)
   * [Debian 10](#debian-10)
   * [CentOS 7](#centos-7)
   * [openSUSE Leap 15.1](#opensuse-leap-151)
3. [Installation](#installation)
   * [Native packages](#native-packages)
   * [Manually](#manually)
     * [Notes on CentOS / RHEL](#notes-on-centos--rhel)
4. [Security considerations](#security-considerations)
5. [Configuration](#configuration)
   * [Basic Authentication](#basic-authentication)
     * [Packages](#packages)
     * [Manually](#manually-1)

Please report any errors you encounter at https://github.com/certtools/intelmq/issues

# Requirements

The following instructions assume the following requirements:

* IntelMQ is already installed
* IntelMQ and IntelMQ Manager will be installed on same machine
* a supported operating system

Supported and recommended operating systems are:
* Debian 9, 10
* Fedora 30, 31, 32
* OpenSUSE Leap 15.1, 15.2
* Ubuntu: 16.04, 18.04, 20.04

Partly supported are:
* CentOS 7
* RHEL 7
See [Notes on CentOS / RHEL](#notes-on-centos--rhel)

# Install Dependencies

If you are using native packages, you can simply skip this section as all dependencies are installed automatically.


## Debian / Ubuntu

```bash
apt-get install git libapache2-mod-php php-json
```

## CentOS / RHEL

```bash
yum install epel-release
yum install git httpd httpd-tools php
```

## Fedora

```bash
dnf install git httpd php php-common php-json

## openSUSE

```bash
zypper install git apache2 apache2-utils apache2-mod_php php-json
```

# Installation

## Native packages

This is only recommended if you also installed intelmq itself with packages.
As you already have the repository configured, you can install the package called `intelmq-manager` using your operating system's package manager.
Complete install instructions for your operating system can be found here:
https://software.opensuse.org/download.html?project=home:sebix:intelmq&package=intelmq-manager

Currently, these operating systems are supported by the packages:
* CentOS 7, install `epel-release` first
* RHEL 7, install `epel-release` first
* Debian 9, 10
* Fedora 30, 31, 32
* openSUSE Leap 15.1, 15.2
* openSUSE Tumbleweed
* Ubuntu 16.04, 18.04, 19.10, 20.04


## Manually

Clone the repository using git and copy the files in the subfolder `intelmq-manager` to the webserver directory (can also be `/srv/www/htdocs/` depending on the used system):
```bash
git clone https://github.com/certtools/intelmq-manager.git /tmp/intelmq-manager
cp -R /tmp/intelmq-manager/intelmq-manager/* /var/www/html/
chown -R www-data.www-data /var/www/html/
```

Add the webserver user (www-data, wwwrun, apache or nginx) to the intelmq group and give write permissions for the configuration files:
```bash
usermod -a -G intelmq www-data
mkdir /opt/intelmq/etc/manager/
touch /opt/intelmq/etc/manager/positions.conf
chgrp www-data /opt/intelmq/etc/*.conf /opt/intelmq/etc/manager/positions.conf
chmod g+w /opt/intelmq/etc/*.conf /opt/intelmq/etc/manager/positions.conf
```

### Allow access to intelmqctl
Give webserver user (www-data, wwwrun, apache or nginx) permissions to execute intelmqctl as intelmq user. Edit the `/etc/sudoers` file and add the adapted following line:
```javascript
www-data ALL=(intelmq) NOPASSWD: /usr/local/bin/intelmqctl
```

The default way of accessing `intelmqctl` program is by command `sudo -u intelmq /usr/local/bin/intelmqctl`. If that does not suit you, you may set an environmental variable `INTELMQ_MANGER_CONTROLLER_CMD` to I.E. `~/.local/bin/intelmqctl` or `PATH=~/.local/bin intelmqctl` or `sudo -u intelmq ~/.local/bin/intelmqctl` or whatever you need.

### Notes on CentOS / RHEL

The manager does currently not work with selinux enabled, you need to deactivate it.
Also, stopping bots does currently not work, see also https://github.com/certtools/intelmq-manager/issues/103

If you can help to fix these issues, please join us!

For RHEL, the packages of CentOS may work better than those for RHEL as there are issues building the packages for RHEL. Help on RHEL is appreciated.

# Security considerations

**Never ever run intelmq-manager on a public webserver without SSL and proper authentication**.

The way the current version is written, anyone can send a POST request and change intelmq's configuration files via sending a HTTP POST request to ``save.php``. Intelmq-manager will reject non JSON data but nevertheless, we don't want anyone to be able to reconfigure an intelmq installation.

Therefore you will need authentication and SSL.

Use IntelMQ Manager **only from a browser that can only access internal, trusted sites** (Due to CSRF, development of a fix is under way, see [#111](https://github.com/certtools/intelmq-manager/issues/111)).

In addition, intelmq currently stores plaintext passwords in its configuration files. These can be read via intelmq-manager.

**Never ever allow unencrypted, unauthenticated access to intelmq-manager**.

# Configuration

## Basic Authentication

### Packages

In DEB-based distributions you will be asked for the password during installation.

In RPM-based distributions, the file will be placed under `/etc/intelmq-manager.htusers` automatically. To set a user-password combination do:
```bash
htpasswd /etc/intelmq-manager.htusers intelmqadmin
```

In both cases the webserver is already configured to use this file for authentication.

### Manually

To create the authentication file:

```bash
htpasswd -c <password file path> <username>
```

To edit an existing one do:

```bash
htpasswd <password file path> <username>
```

on IntelMQ Manager edit the httpd.conf and insert

```javascript
AuthType basic
AuthName "IntelmMQ Manager"

AuthBasicProvider file
AuthUserFile <password file path>
Require valid-user
```

After this is done you'll have to put the user/pass combination you have created with htpasswd to access the web pages of IntelMQ Manager. To use other authentication methods visit: http://httpd.apache.org/docs/2.4/howto/auth.html

## Content-Security-Policy Headers

### Manually

It is recommended to set these two headers for all requests:

```
Content-Security-Policy: script-src 'self'
X-Content-Security-Policy: script-src 'self'
```
