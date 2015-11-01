Use the HipChat plugin to send a message to a HipChat channel when a build 
completes. You will need to create a room authentication token and pass
that plus the room's name or ID in.

The following parameters are used to configuration the notification:

* **room_id_or_name** - the room's name or numerical ID
* **room_auth_token** - an auth token for the room
* **message_notify** - if `true`, noisily alert room members 

The following is a sample Slack configuration in your .drone.yml file:

```yaml
notify:
  hipchat:
    image: gtaylor/drone-hipchat
    room_auth_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    room_id_or_name: 1234567
    message_notify: true
```
