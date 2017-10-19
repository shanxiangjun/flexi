import os
import subprocess
import logging
import tools

class Loop() :
    successful = True
    errors = []
    globalnumber = 0

    def __init__(self, parent, name, number = -1, mkdir=True) :
        self.number = number
        self.parent = parent
        if self.parent :
            parent_dir = self.parent.target_directory
        else :
            parent_dir = "reggie_outdir"
        if number >= 0 :
            self.target_directory = os.path.join(parent_dir, "%s_%04d" %(name, number))
        else :
            self.target_directory = os.path.join(parent_dir, name)
        self.skip = os.path.exists(self.target_directory)

        if mkdir :
            if not os.path.exists(self.target_directory) :
                os.makedirs(self.target_directory)  # create example directory

    def execute_cmd(self, cmd):
        """Execute an external program specified by 'cmd'. The working directory of this program is set to self.target_directory.
        Returns return_code, stdout, stderr of the external program.
        """
        log = logging.getLogger('logger')

        workingDir = os.path.abspath(self.target_directory)
        log.debug(workingDir)
        log.debug(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=workingDir)
        self.stdout = []
        self.stderr = []
        for line in iter(process.stdout.readline, '') :
            log.info(line.rstrip())
            self.stdout.append(line)
        process.stdout.close()
        
        for line in iter(process.stderr.readline, '') :
            self.stderr.append(line)
        process.stderr.close()

        self.return_code = process.wait()

        # write std.out and err.out to disk
        self.stdout_filename = os.path.join(self.target_directory,"std.out")
        f = open(self.stdout_filename, 'w')
        for line in self.stdout :
            f.write(line)
        f.close()
        if self.return_code != 0 :
            self.result=tools.red("Failed.")
            self.stderr_filename = os.path.join(self.target_directory,"std.err")
            f = open(self.stderr_filename, 'w')
            for line in self.stderr :
                f.write(line)
            f.close()
        else :
            self.result=tools.blue("Successful.")
        print self.result

        return self.return_code, self.stdout, self.stderr

