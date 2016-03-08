# Configurator - Simple Python Configuration


*   Supports any number of configuration objects
*   Supports overriding via environment variables
 
 
### Create a configuration object using two dictionaries 
    config = Configurator(
        [
            {"app": {"env": "dev"}},
            {"app": {"env": "local"}}
        ]
    )
    print(config.app.env) # prints out local
    print(json.dumps(config, indent=2))
    # prints out the following
    {
      "app": {
        "env": "local"
      }
    }    
        
### Create a configuration object using two dictionaries w/ environment vars
    # add an environment variable
    export CUSTOM_app__env="production"
    ...
    config = Configurator(
        [
            {"app": {"env": "dev"}},
            {"app": {"env": "local"}}
        ],
        env_var_pfx="CUSTOM",
        auto_cast=True
    )
    print(config.app.env) # prints out "production" 
    print json.dumps(config, indent=2)        
    # prints out the following
    {
        "app": {
            "env": "production"
        }
    }