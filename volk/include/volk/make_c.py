from xml.dom import minidom
import string
from volk_regexp import *


def make_c(funclist, taglist, arched_arglist, retlist, my_arglist, fcountlist) :
    tempstring = "";
    tempstring = tempstring + '/*this file is auto generated by volk_register.py*/';
    tempstring = tempstring + '\n\n#include<volk/volk.h>\n';
    tempstring = tempstring + '#include<volk/volk_tables.h>\n';
    tempstring = tempstring + '#include<volk/volk_typedefs.h>\n';
    tempstring = tempstring + '#include<volk/volk_registry.h>\n';
    tempstring = tempstring + '#include<string.h>\n';
    for func in funclist:
        tempstring = tempstring + "#include<volk/" + func + ".h>\n" ;
    tempstring = tempstring + '\n';

    tempstring = tempstring + "static inline unsigned int volk_get_index(const char** indices, const char* arch, const int* arch_defs) {\n";
    tempstring = tempstring + "    int i = 1;\n"
    tempstring = tempstring + "    for(;i<arch_defs[0];++i){\n"
    tempstring = tempstring + "        if (strcmp(arch, indices[i]) == 0) {\n"
    tempstring = tempstring + "            return i;\n"
    tempstring = tempstring + "        }\n"
    tempstring = tempstring + "    }\n"
    tempstring = tempstring + "    return 0;\n"
    tempstring = tempstring + "}\n"

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

        tempstring = tempstring + "static const char* " + funclist[i] + "_indices[] = {\n";
        
        tags_counter = 0;    
        for arch_list in fcountlist[i]:
            tempstring = tempstring + "#if LV_HAVE_"
            for ind in range(len(arch_list)):
                
                tempstring = tempstring + arch_list[ind];
                if ind < len(arch_list) - 1:
                    tempstring = tempstring + " && LV_HAVE_";
                
            tempstring = tempstring + "\n \"" + str(taglist[i][tags_counter]) + "\",\n#endif\n";
            tags_counter = tags_counter + 1;
                
        lindex = tempstring.rfind(",");
        tempstring = tempstring[0:lindex] + string.replace(tempstring[lindex:len(tempstring)], ",", "");
        tempstring = tempstring + "};\n\n";
                                                                          
        tempstring = tempstring + retlist[i] + "inline " + funclist[i] + "_manual" + arched_arglist[i] + '\n';
        tempstring = tempstring + "return " + funclist[i] + "_archs[volk_get_index(" + funclist[i] + "_indices, arch, " + funclist[i] + "_arch_defs)](" + my_arglist[i] + ");" + "\n}\n";
    
        tempstring = tempstring + retlist[i] + "inline " + funclist[i] + replace_arch.sub("", arched_arglist[i]) + '\n';
    
        tempstring = tempstring + funclist[i] + "_archs[" + funclist[i] + "_func_table](" + my_arglist[i] + ");" + '\n';
        tempstring = tempstring + "}\n\n";                                       
    
    return tempstring;
