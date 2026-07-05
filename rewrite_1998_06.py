import yaml
import re

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1998-06-bad-aibling-germany.yaml", "r") as f:
    data = yaml.safe_load(f)

titles = {
    '354': "Approve new project leaders and project editors",
    '355': "Instruct project leaders to develop proposals and establish a registration authority",
    '356': "Publish SC 4 organizational handbook in a Web-based format",
    '357': "Thank Sharon Kemmerer for her service as SC 4 Secretary",
    '358': "Add wording to SC 4 Handbook Section 2.3 on normative references",
    '359': "Approve PWI proposal for history-based shape modeling",
    '360': "Approve Bruno Schilli as Deputy Convener of WG 3",
    '361': "Define ISO 10303 Release 2.0 parts and schedule",
    '362': "Extend SEDS procedures to cover standing documents and technical reports",
    '363': "Establish active two-way liaison with European Marine STEP Association",
    '364': "Establish active two-way liaison with ISO/IEC JTC 1/WG 4",
    '365': "Forward Technical Corrigendum 2 for ISO 10303-203 to ISO for publication",
    '366': "Approve PWI on Process Plant Operations and Maintenance",
    '367': "Thank Meinolf Groepper for his service and liaison work",
    '368': "Note IEC Sector Board 3 work and encourage global strategy",
    '369': "Approve PWI on Dimensional Inspection Information Exchange",
    '370': "Endorse extension of ISO/IEC UN/ECE MoU into electronic business",
    '371': "Request Secretariat report on anticipated electronic operation of SC 4",
    '372': "Approve MoU documented in SC 4 N 732",
    '373': "Instruct Change Management Team to check New Work Item proposals",
    '374': "Approve PWI on STEP Modularization",
    '375': "Approve PWI in furniture product data and project data",
    '376': "Request statements of user requirements and milestones for next SC 4 release",
    '377': "Ensure STEP parts are Year 2000 compliant",
    '378': "Thank Bernd and Ramona Wenzel and EuroSTEP support staff"
}

def clean_message(msg):
    if msg.strip() == ".":
        return None
        
    # Carefully replace single newlines that are just PDF wraps.
    # Exclude newlines before | or after |
    lines = msg.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            new_lines.append('')
        else:
            if new_lines and new_lines[-1] != '' and not new_lines[-1].startswith('|') and not line.startswith('|') and not line.startswith('*') and not line.startswith('▸'):
                new_lines[-1] = new_lines[-1] + ' ' + line
            else:
                new_lines.append(line)
    
    msg = '\n'.join(new_lines)
    msg = msg.replace('▸', '*')
    
    # ensure multiple newlines are just \n\n
    msg = re.sub(r'\n{3,}', '\n\n', msg)
    
    # Append newline so yaml literal block uses | instead of |-
    return msg.strip() + '\n'

for res in data['resolutions']:
    res['title'] = titles.get(res['identifier'], res['title'])
    
    new_actions = []
    for act in res['actions']:
        if act['message'].strip() == '.':
            continue
        act['message'] = clean_message(act['message'])
        
        # fix action types for acclamations
        if res['identifier'] in ['357', '367', '378'] and act['type'] == 'resolves':
            act['type'] = 'thanks'
            
        new_actions.append(act)
    
    res['actions'] = new_actions

class LiteralString(str):
    pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(LiteralString, literal_presenter)

# Apply LiteralString to all messages
for res in data['resolutions']:
    for act in res.get('actions', []):
        act['message'] = LiteralString(act['message'])
    for cons in res.get('considerations', []):
        cons['message'] = LiteralString(cons['message'])

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1998-06-bad-aibling-germany.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)

