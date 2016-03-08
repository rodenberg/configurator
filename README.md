# Configurator - Simple Python Configuration

This is a simple python module used to cascade override a list of dictionaries

Supports overriding values using environment variables.

    config = Configurator(
        [
            {"app": {"env": "dev"}},
            {"app": {"env": "local"}}
        ]
    )
    
    print json.dumps(config, indent=2)
    # prints out the following
    {
      "app": {
        "env": "local"
      }
    }    
        
    
    # add an environment variable
    export CUSTOM_app__env="production"
    
    config = Configurator(
        [
            {"app": {"env": "dev"}},
            {"app": {"env": "local"}}
        ],
        env_var_pfx="CUSTOM",
        auto_cast=True
    )
    
    print json.dumps(config, indent=2)        
    # prints out the following
    {
        "app": {
            "env": "production"
        }
    }