### Generator features

| Category          | Feature                   | In Scope | Status |
| ----------------- | ------------------------- | -------- | ------ |
| Connection type   | with service connector    | `✔`   | `✔` |
|                   | config service directly   | `✔`   | `✔` |
| Interface         | API                       | `✔`   | `✖` |
|                   | library                   | `✔`   | `✖` |
| Multiple targets  | of different types        | `✔`   | `✔` |
|                   | of same types             | `✔`   | `✖` |
| Existing resource | sync to bicep parameters | `✔`   | `✖` |

### Connection features

| Category         | Feature           | In Scope | Status |
| ---------------- | ----------------- | -------- | ------ |
| compute type     | webapp            | `✔`   | `✔` |
|                  | ... others ...    | `✔`   | `✖` |
| target type      | storage, postgres | `✔`   | `✔` |
|                  | ... others ...    | `✔`   | `✖` |
| auth type        | secret / systemMI | `✔`   | `✔` |
|                  | userMI / SP       | `✖`   | `✖` |
| client type      | python            | `✔`   | `✔` |
|                  | ... others ...    | `✔`   | `✖` |
| keyvault         | secret store      | `✔`   | `✖` |
|                  | secret reference  | `✖`   | `✖` |
| network solution | public            | `✔`   | `✔` |
|                  | vnet              | `✖`   | `✖` |
| customizations   | key names         | `✖`   | `✖` |
|                  | roles             | `✖`   | `✖` |
