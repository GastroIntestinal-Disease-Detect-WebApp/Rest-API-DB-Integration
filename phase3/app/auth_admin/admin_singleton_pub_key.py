class ClassicSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassicSingleton, cls).__new__(cls)
            
            print("Hey there reading a file !!!")
            
            fp = open('/Users/adityaved/prj_ws/my_git_hub_repos/sem6/GitHubOrganisation_MP/AuthenticationSystem-Microservice/phase2/protected_routes_microservice/auth/jwt_id_rsa_key.pub', 'r')
            # Initialize the data attribute
            cls._instance.public_key = fp.read()
            
            fp.close()
        return cls._instance

    def get_data(self):
        return self.public_key
