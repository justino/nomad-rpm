# RPM Spec for Nomad

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/nomad`
* Config: `/etc/nomad.d/`
* Shared state: `/var/lib/nomad/`
* Sysconfig: `/etc/sysconfig/nomad`

# Versioning

The version number is hardcoded into the SPEC, however should you so choose, it can be set explicitly by passing an argument to `rpmbuild` directly:

```bash
$ rpmbuild --define "_version 0.8.10"
```

# Build

* Build the Docker image. Note that you must amend the `Dockerfile` header if you want a specific OS build (default is `centos7`).
    ```bash
    docker build -t nomad:build .
    ```

* Run the build.
    ```bash
    docker run -v $PWD:/build nomad:build
    ```

* Retrieve the built RPM from `$PWD/rpmbuild/RPMS`.

# Run

* Install the RPM.
* Put config files in `/etc/nomad.d/`.
* Change command line arguments to nomad in `/etc/sysconfig/nomad`.
  * Add `-bootstrap` **only** if this is the first server and instance.
* Start the service and tail the logs `systemctl start nomad.service` and `journalctl -f`.
* To enable at reboot `systemctl enable nomad.service`.
* Nomad may complain about the `GOMAXPROCS` setting. This is safe to ignore;
however, the warning can be supressed by uncommenting the appropriate line in
`/etc/sysconfig/nomad`.

## Config

Config files are loaded in lexical order from the `config-dir`. A
sample config is provided.

# More info

See the [nomadproject.io](https://www.nomadproject.io) website.
