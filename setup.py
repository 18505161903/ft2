from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "ft2",      #这里是pip项目发布的名称
    version = "1.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "ft2"),
    description = "excel回测",
    long_description = "excel回测",
    license = "excel回测",

    url = "https://github.com/18505161903/ft2",     #项目相关文件地址，一般是github
    author = "392161222",
    author_email = "392161222@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []         #这个项目需要的第三方库
)