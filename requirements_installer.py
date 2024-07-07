import pip

def install_library(name):
    requirements = ["install"]
    for i in name.split():
        requirements.append(i)
    
    print(requirements)
    pip.main(requirements)
