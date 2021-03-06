from xml.dom import minidom
import string
from volk_regexp import *


def make_runtime_c(funclist, taglist, arched_arglist, retlist, my_arglist, fcountlist) :
    tempstring = "";
    tempstring = tempstring + '/*this file is auto generated by volk_register.py*/';

    
    tempstring = tempstring + '\n\n#include<volk/volk_runtime.h>\n';
    tempstring = tempstring + '#include<volk/volk_config.h>\n';
    tempstring = tempstring + "#include<volk/volk_config_fixed.h>\n";
    tempstring = tempstring + '#include<volk/volk_cpu.h>\n';
    tempstring = tempstring + '#include<volk_init.h>\n';
    tempstring = tempstring + '#include<volk/volk_registry.h>\n';

    for func in funclist:
        tempstring = tempstring + "#include<volk/" + func + ".h>\n" ;
    tempstring = tempstring + '\n';

    tempstring = tempstring + "struct VOLK_RUNTIME volk_runtime;\n";
    
    for i in range(len(funclist)): 
        tempstring = tempstring + "static const " + replace_volk.sub("p", funclist[i]) + " " + funclist[i] + "_archs[] = {\n";
        
        tags_counter = 0;    
        for arch_list in fcountlist[i]:
            tempstring = tempstring + "#if LV_HAVE_"
            for ind in range(len(arch_list)):
                
                tempstring = tempstring + arch_list[ind];
                if ind < len(arch_list) - 1:
                    tempstring = tempstring + " && LV_HAVE_";
                
            tempstring = tempstring + "\n " + funclist[i] + "_" + str(taglist[i][tags_counter]) + ",\n#endif\n";
            tags_counter = tags_counter + 1;
                
        lindex = tempstring.rfind(",");
        tempstring = tempstring[0:lindex] + string.replace(tempstring[lindex:len(tempstring)], ",", "");
        tempstring = tempstring + "};\n\n";


        tempstring = tempstring + retlist[i] + "default_acquire_" + funclist[i] + replace_arch.sub("", arched_arglist[i]) + '\n';
        tempstring = tempstring + "volk_runtime." + funclist[i] + " = " + funclist[i] + "_archs[volk_rank_archs(" + funclist[i] + "_arch_defs, volk_get_lvarch())];\n" + "return " + funclist[i] + "_archs[volk_rank_archs(" + funclist[i] + "_arch_defs, volk_get_lvarch())](" + my_arglist[i] + ");" + '\n}\n';
    
    return tempstring;
