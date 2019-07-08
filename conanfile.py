from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

#
# This is the conan recipe for libcci. This recipe is for the older
# version of cci which does not use Cmake or Git. The source is
# downloaded from ftp.
#
#
# This will need to be modified for the newer versions which use git
#
class xdrfileConan(ConanFile):
    name = "xdrfile"
    version = "1.1.4"
    sha256 = "ac18cbf4ae9a22a22516351f5b5ce01dbd8cf0f4faaf36523c6ed2539ed4dcff"

    #ftp://ftp.gromacs.org/pub/contrib/xdrfile-1.1.4.tar.gz

    homepage = "https://github.com/CCI/cci"

    ftp_address = "ftp.gromacs.org"
    filename = "xdrfile-{0}.tar.gz".format(version)
    ftp_file_path = "pub/contrib/{}".format(filename)

#    url_file_path = "ftp://ftp.gromacs.org/pub/contrib/xdrfile-1.1.4.tar.gz"
#    url_file_path = "ftp://ftp.gromacs.org/pub/contrib/xdrfile-{0}.tar.gz".format(version)
    #url_file_path = "{0}/archive/v{1}.tar.gz".format(homepage, version)

    license = "LGPL"
    url = "https://github.com/GavinNL/conan-xdrfile"

    description = "A High-Performance Communication Interface for HPC and Data Centers"

    options = {
        "shared": [True, False]
    }

    default_options = (
         "shared=True"
    )

    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"

    _source_subfolder = "source_subfolder"


    def configure(self):
        # This is a C library, so remove the libcxx option
        del self.settings.compiler.libcxx

        print("Running configure()")

        if self.settings.os != "Linux":
            raise Exception("Only Linux supported")

    def source(self):
#        print("Downloading: " + self.url_file_path)
        tools.ftp_download(self.ftp_address, self.ftp_file_path)
#        tools.get(self.url_file_path, sha256=self.sha256)
        #tools.check_sha256(self.file_name, self.sha256)
        tools.untargz(self.filename)
        os.rename("xdrfile-{0}".format(self.version), self._source_subfolder)



    def build(self):
        ab = AutoToolsBuildEnvironment(self)

        configure_args = []
        if self.options.shared:
            configure_args.append('--enable-static=no')
            configure_args.append('--enable-shared=yes')
        else:
            configure_args.append('--enable-static=yes')
            configure_args.append('--enable-shared=no')

        #configure_args = [ '--enable-static=no', "--enable-shared=yes"]

        with tools.chdir( self._source_subfolder ):
            ab.configure(args=configure_args)
            ab.make(target="install")

    def package(self):
        self.copy("*COPYING*", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = ["xdrfile"]
        #self.env_info.ALSA_CONFIG_DIR = os.path.join(self.package_folder, "share", "alsa")
