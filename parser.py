import re

tokens = []
opening_tags = []
# closing_tags = []

single = ["input","link","img","meta","br","hr"]

dift = {
"a":["href","target","charset","coords","download","hreflang","media","name","rel","rev","shape","type"],
"div":["align"],
"p":["align"], 
"button":["autofocus","disabled","form","formaction","formenctype","formmethod","formnovalidate","formtarget","name","type","value"],
"body":["alink","background","bgcolor","link","text","vlink"],
"input":["accept","align","alt","autocomplete","autofocus","checked","dirname","disabled","form","formaction","formenctype","formmethod","formnovalidate","formtarget","height","list","max","maxlength","min","multiple","name","pattern","placeholder","readonly","required","size","src","step","type","value","width"],
"select":["autofocus","disabled","form","multiple","name","required","size"],"form":["accept","accept-charset","action","autocomplete","enctype","method","name","novalidate","target"],
"img":["src","align","alt","border","crossorigin","height","width","hspace","ismap","longdesc","sizes","srcset","usemap","vspace"],
"script":["async","charset","defer","src","type","xml:space"],
"textarea":["autofocus","cols","dirname","disabled","form","maxlength","name","placeholder","readonly","required","rows","wrap"],
"link":["charset","crossorigin","href","hreflang","media","rel","rev","sizes","target","type"],
"ol":["compact","reversed","start","type"],
"ul":["compact","reversed","start","type"],
"li":["type","value"],
"table":["align","bgcolor","border","cellpadding","cellspacing","frame","rules","summary","width"],
"td":["abbr","align","axis","bgcolor","char","charoff","colspan","headers","height","width","nowrap","rowspan","scope","valign"],
"tr":["align","bgcolor","char","charoff","valign"]
}

global_attr = ["accesskey","class","contenteditable","contextmenu","data","dir","draggable","dropzone","hidden","id","lang","spellcheck","style","tabindex","title","translate"]


symbol_table = []
i=-1
j =-1
attributes = []
f = open("test.html")
st = f.readlines()
l=0
for line in st:
    l+=1
    op = re.findall('<[^!^-^\/].*?>',line)
    if(op !=[]):
        for item in op:
            i+=1
            item2 = item.replace(" "," , ")
            #y = item.split(" ")
            #if(item[-1] != '>'):
                #y[0]+='>'
            #print(type(y[0]))
            s = item2[1:-1]+"_"+str(i)

            symbol_table.append((item2,'op_tag',0,i,l,s))
            opening_tags.append(item)
            opening_tags.append(i)
            #for x in re.findall('[a-z]*?=".*?"',item):
            #symbol_table.append((x.split('=')[0],'attribute',x.split('=')[1],i,l))
    cl = re.findall('</.*?>',line)
    if(cl !=[]):
        for item in cl:
            j+=1
            symbol_table.append((item,'cl_tag',0,j,l,item[1:-1]))


    
        
   


# for sym in symbol_table:
    #print(sym)


tags = [x[5] for x in symbol_table if (x[1]=='op_tag' or x[1] == 'cl_tag')]

#print(tags)


for i in range(len(opening_tags)):
    x=opening_tags[i]
    #print(x,"\n")
    if(type(x)== int):
        continue

    y = []
    y.append(x.split(" ")[0])

    y.extend(re.findall("[a-zA-Z]+\=\"[^\"]+\"[\ >]",x))
    if(y == []):
        continue
    #print(y)
    

    #tokens.append(y[0][0])
    y[0] = y[0][1:]

    for j in range(1,len(y)):
        temp=y[j].split("=")
        if(temp[0] not in global_attr and y[0] in dift and temp[0]!='style'):
            if(temp[0] not in dift[y[0]]):
                k = i+1;
                while(type(opening_tags[k])!=int):
                    k+=1
                print("\nWARNING!Line no.",opening_tags[k],temp[0],"is not an attribute of",y[0],"!\n")
        #tokens.append(y[j])
    #y.append(y[0][0])
    #tokens.append(y[len(y)-1][:-1])
    #tokens.append(y[len(y)-1][-1])



import json

token = []  #stack
dom = {}   #JSON dict



for item in tags[:-1]:
    if(item[0]!='/'):
        flag = 0
        for sing in single: 
            if sing in item.split(" ")[0]:
                flag = 1
                if(token[-1] not in dom):
                    dom[token[-1]] = [item]
                else:
                    dom[token[-1]].append(item)
                continue
        if(flag == 0):
            token.append(item)
    else:
        a = token.pop()
        if(a in dom):   
            temp = {}
            temp[a] = dom[a]
            del dom[a]
            if(token[-1]not in dom):
                dom[token[-1]] = [temp]
            else:
                dom[token[-1]].append(temp)
        else:
            if(token[-1] not in dom):
                dom[token[-1]] = [a]
            else:
                dom[token[-1]].append(a)
           
        
    #print(token)
    #print(dom)
    #print()
jso = json.dumps(dom)
jso = jso.replace(':',", children :")
jso = jso.replace('{"', '{ text: { name : "')
jso = jso.replace('["', '[ { text: { name : "')
jso = jso.replace(', "', ', { text: { name : "')
jso = jso.replace('",', '"},')
jso = jso.replace('}, {', '}}, {')
jso = jso.replace('"]}', '"}}]}')
jso = jso.replace('"],', '"}}],')
jso = jso.replace(']}}', ']}')


jso.replace('name','"name"')
jso.replace('text','"text"')
jso.replace('children','"children"')

repl = re.findall('"[a-z0-9A-Z]+\ ,',jso)

for item in repl:
    jso = jso.replace(item,item[:-1]+'", type: "')

#print(repl)


print(jso)