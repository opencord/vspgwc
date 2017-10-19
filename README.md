# Virtual Serving PDN Gateway - Control Plane Service

## Onboarding

To onboard this service in your system, you can add the service to the `mcord.yml` profile manifest:

```
xos_services:
  - name: vspgwc
    path: orchestration/xos_services/vspgwc
    keypair: mcord_rsa
```
