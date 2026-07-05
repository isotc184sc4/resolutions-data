import ruamel.yaml
from ruamel.yaml.scalarstring import LiteralScalarString
import glob
import re

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.representer.ignore_aliases = lambda *data: True

titles = {
    '1018': 'Approve Project Leaders and Editors for SC 4 Projects',
    '1019': 'Appoint Véronique Dubillot as Quality Committee Convenor',
    '1020': 'Appoint Melissa Harvey as Quality Committee Secretary',
    '1021': 'Reappoint Jochen Haenisch as WG 12 and WG 21 Deputy Convenor',
    '1022': 'Appoint David Leal as Liaison Officer to NAFEMS',
    '1023': 'Apply 24-month development track to ISO 15926-14',
    '1024': 'Extend term of AHG 1 Core Industrial Data Set of Terms',
    '1025': 'Create Task Force for ISO 10303 SMRL Architecture innovation',
    '1026': 'Establish PWI for Ontology for geometry and topology',
    '1027': 'Cancel ISO 8000-64 and launch NP Ballot',
    '1028': 'Prepare report to combine ISO 8000 master data standards',
    '1029': 'Identify experts to review ISO/DIS 29002 Edition 2',
    '1030': 'Document mapping between ISO 10303 STEP and ISO 23952 QIF',
    '1031': 'Circulate CIB for draft ISO Committee Specific Procedure',
    '1032': 'Appoint Yoshiaki Sonoda as Liaison Officer to IEC SC 3D',
    '1033': 'Appoint Mario Tucci as SC 4 Implementation Forum Deputy Convenor',
    '1034': 'Create Ad hoc team for Nuclear Digital Ecosystem Specification',
    '1035': 'Call for requirements on data visualization for industrial artefacts',
    '1036': 'Apply 8-week CD ballot duration to ISO 10303-59 ed3',

    '1037': 'Approve Project Leaders and Editors for SC 4 Projects',
    '1038': 'Apply 8-week ballot duration to NP ballots',
    '1039': 'Appoint Nils Sandsmark as WG 3 Deputy Convenor',
    '1040': 'Appoint Anne Dourgnon as WG 13 Deputy Convenor',
    '1041': 'Appoint Dave Loffredo as WG 11 Convenor',
    '1042': 'Extend term of AHG 1 and request final report',
    '1043': 'Extend term of AHG 2 Nuclear Digital Ecosystem Specification',
    '1044': 'Deprecate SC4N0535 and SC4N1290 as standing documents',
    '1045': 'Create Task Force for SC 4 Reference Model for Industrial Data',
    '1046': 'Organize meeting on digital handover for nuclear power plants',
    '1047': 'Launch ISO 15926-4 ed.3 on 24-month track',
    '1048': 'Apply 24-month development track to ISO 10303-17',
    '1049': 'Request 9-month extension for ISO 10303-243 from ISO TMB',
    '1050': 'Notify ISO CS of errors in ISO 10303-242 ed2',
    '1051': 'Request 9-month extension for ISO 10303-238 ed2',

    '1052': 'Appoint Hayley Thompson as WG 23 Deputy Convenor',
    '1053': 'Appoint Tim King as liaison representative to ISO/IEC JTC 1/SC 7',
    '1054': 'Extend term of AHG 1 on Core Industrial Data Set of Terms',
    '1055': 'Extend term of AHG 2 on Nuclear Digital Ecosystem Specification',
    '1057': 'Initiate review of Liaison appointments through SC 4 Newsletter',
    '1058': 'Approve ISO/AWI 17506 to move to DIS ballot',
    '1059': 'Move ISO 10303-17 from SDT 24 to SDT 36 development track',
    '1060': 'Request 9-month extension for ISO 10303-209 ed3 from ISO TMB',
    '1061': 'Approve Jira/Git procedure for select SC 4 projects',
    '1062': 'Circulate CIB for draft JWG 24 procedure for managing standards',

    '1063': 'Apply 8-week ballot duration to NP ballots',
    '1064': 'Appoint Convenors and Deputy Convenors for SC 4 Working Groups',
    '1065': 'Request ISO TMB place ISO 10303-209 ed3 on hold for six months',
    '1066': 'Change ISO 8000-110 ed2 to SDT 36 development track',
    '1067': 'Request 9-month schedule extension for ISO/TS 23301 from ISO TMB',
    '1068': 'Create Advisory Group on Core terminology for industrial data',
    '1069': 'Extend term of Ad Hoc Group 2 on Nuclear Digital Ecosystem Specification',
    '1070': 'Conduct review of SC4N1167 Industrial Data Framework via CIB',
    '1071': 'Launch combined NP/CD ballot for ISO 10303-239 ed3',
    '1072': 'Launch minor revisions to ISO 10303-210, 10303-238, and 10303-242',
    '1073': 'Establish Ad Hoc Group on UUID management for industrial data',
    '1074': 'Update SC 4 Handbook standing documents via CIB',
    '1075': 'Conclude ISO 8000-2 Vocabulary Living Lab and accept final report',
    '1076': 'Conclude ISO 15926-4 Uniform Resource Identifiers Living Lab'
}

def is_acclamation(act_type, msg):
    if act_type == 'appreciation' or act_type == 'thanks':
        return True
    lower_msg = msg.lower().strip()
    if lower_msg.startswith('sc 4 expresses its appreciation'):
        return True
    if lower_msg.startswith('sc4 expresses its appreciation'):
        return True
    if lower_msg.startswith('sc 4 also wishes to express thanks'):
        return True
    if lower_msg.startswith('sc 4 expresses its profound thanks'):
        return True
    if lower_msg.startswith('wishes brian the best'):
        return True
    if lower_msg.startswith('sc 4 sincerely appreciates'):
        return True
    return False

def get_acclaim_title(msg):
    lower_msg = msg.lower()
    if 'véronique dubillot' in lower_msg and 'secretary' in lower_msg:
        return 'Thank Véronique Dubillot for Quality Committee Secretary service'
    if 'anna moreno' in lower_msg:
        return 'Thank Anna Moreno for Implementation Forum service'
    if 'sc 4 liaisons' in lower_msg and 'presentations' in lower_msg:
        return 'Thank SC 4 Liaisons for presentations at 78th Plenary'
    if 'open technical forum' in lower_msg:
        return 'Thank Open Technical Forum participants'
    if 'industry day' in lower_msg:
        return 'Thank SC 4 Industry Day presenters and facilitators'
    if 'eccma' in lower_msg:
        return 'Thank ECCMA and Hotel MdR for organizing 78th Plenary'
    if 'liaisons and reports' in lower_msg and '79th' in lower_msg:
        return 'Thank SC 4 Liaisons for reports to 79th Plenary'
    if 'liaisons and reports' in lower_msg and '80th' in lower_msg:
        return 'Thank SC 4 Liaisons for reports to 80th Plenary'
    if 'liaisons and reports' in lower_msg and '81st' in lower_msg:
        return 'Thank SC 4 Liaisons for reports to 81st Plenary'
    if 'melissa harvey' in lower_msg and 'website' in lower_msg:
        return 'Thank Melissa Harvey and ISO Web team for website'
    if 'microsoft teams' in lower_msg:
        return 'Thank JWG 16 for evaluating Microsoft Teams'
    if 'digital tools' in lower_msg:
        return 'Thank WG 13/23 for evaluating digital tools'
    if 'brian stanton' in lower_msg:
        return 'Thank Brian Stanton for 15 years as Editorial Program Manager'
    if 'brian the best' in lower_msg:
        return 'Extend best wishes to Brian Stanton in continuing ISO role'
    if 'anne-françoise cutting-decelle' in lower_msg:
        return 'Thank Anne-Françoise Cutting-Decelle for JWG 8 Convenor service'
    if 'anne dourgnon' in lower_msg:
        return 'Thank Anne Dourgnon for WG 13 Deputy Convenor service'
    if 'ecommittees' in lower_msg:
        return 'Thank ISO CS and Documents team for eCommittees transition'
    if 'iso it' in lower_msg:
        return 'Thank ISO IT for supporting Committee Innovations with Living Labs'
    if 'sponsorship and enthusiasm' in lower_msg:
        return 'Thank ISO staff for supporting innovation'
    if 'nils sandsmark' in lower_msg and 'multi-group' in lower_msg:
        return 'Thank Nils Sandsmark for organizing multi-group coordination meeting'
    if 'soonhung han' in lower_msg and 'christophe mouton' in lower_msg:
        return 'Thank Soonhung Han and Christophe Mouton for JWG 16 leadership exchange'
    if 'allison barnard feeney' in lower_msg and 'melissa harvey' in lower_msg:
        return 'Thank Allison Barnard Feeney and Melissa Harvey for LD Eicher award submission'
    if 'virtual plenary meeting successfully' in lower_msg:
        return 'Thank experts and leaders for virtual plenary success'
    return 'Express appreciation'

def clean_text(text):
    if not text: return ""
    text = re.sub(r'ACKNOWLEDGEMENTS and APPRECIATIONS\s*ACCLAMATION\s*', '', text)
    text = re.sub(r'ACCLAMATION\s*', '', text)
    text = text.replace('ACKNOWLEDGEMENTS and APPRECIATIONS', '')
    
    lines = text.split('\n')
    cleaned_lines = []
    
    buffer = ""
    for line in lines:
        l = line.strip()
        if not l:
            if buffer:
                cleaned_lines.append(buffer)
                buffer = ""
            cleaned_lines.append("") 
        elif l.startswith('*') or l.startswith('-') or l.startswith('1.') or l.startswith('2.') or l.startswith('3.') or l.startswith('4.') or l.startswith('5.'):
            if buffer:
                cleaned_lines.append(buffer)
                buffer = ""
            buffer = l
        elif "Project" in l and "Approval" in text: 
            if buffer:
                cleaned_lines.append(buffer)
                buffer = ""
            buffer = l
        else:
            if buffer:
                if buffer.endswith('-'):
                    buffer = buffer[:-1] + l
                else:
                    buffer += " " + l
            else:
                buffer = l
                
    if buffer:
        cleaned_lines.append(buffer)
        
    res = "\n".join(cleaned_lines)
    res = re.sub(r'\n{3,}', '\n\n', res)
    return res.strip()

def process_file(filepath, year_month):
    with open(filepath, 'r') as f:
        data = yaml.load(f)
        
    acclaim_idx = 1
    new_resolutions = []
    
    for res in data.get('resolutions', []):
        ident = res.get('identifier', '')
        if ident in titles:
            res['title'] = titles[ident]
            
        new_actions = []
        if 'considerations' not in res:
            res['considerations'] = []
            
        raw_actions = res.get('actions', [])
        
        for act in raw_actions:
            msg = act.get('message', '').strip()
            
            if msg == '.' or msg == '':
                 continue
            if len(msg) < 100 and (res.get('title', '') in msg or msg in res.get('title', '')):
                 if act.get('type', '') == 'resolves':
                     continue
            elif msg == 'Approval of Project Leaders for SC 4 Projects' or msg == 'Appointment of Quality Committee Convenor' or msg == 'Appointment of Quality Committee Secretary' or msg == 'Reappointment of WG 12/21 Deputy Convenor' or msg == 'Appointment of Liaison Officer to NAFEMS' or msg == 'Extend the term of the Ad Hoc Group onCore Industrial Data Set of Terms' or msg == 'Create a Task Force for SMRL' or msg == 'Establish PWI on ontology for geometry and topology' or msg == 'Cancellation of ISO 8000-64' or msg == 'Cancellation of ISO 8000-110 Edition 2 project' or msg == 'Review of ISO/DIS 29002' or msg == 'Initiate CIB for SC 4 Committee Specific Procedure' or msg == 'Reestablish Liaison Officers to IEC SC 3D' or msg == 'Leadership Changes for SC 4 Implementation Forum' or msg == 'Ad Hoc Group to draft NWI Nuclear Digital Ecosystem Specification' or msg == 'Call for requirements for data visualization in the context of industrial artefacts' or msg == 'CD Ballot duration of ISO 10303-59 ed3' or msg == 'To establish reduced ballot period for New Proposal' or msg == 'Appointment of Deputy Convenor to WG 3' or msg == 'Appointment of Deputy Convenor to WG 13' or msg == 'Appointment of Convenor to WG 11' or msg == 'To extend the term of AHG 1' or msg == 'Deprecate SC4N0535 and SC4N1290 as standing documents' or msg == 'Liaison appointment review' or msg == 'Extend term of the Ad Hoc Group 2 on Nuclear Digital Ecosystem' or msg == 'Extend term of Ad Hoc Group 1 on Core Industrial Data Set of Terms' or msg == 'Appointment of Deputy Convenor to WG 23' or msg == 'Approve ISO/AWI 17506 to move to DIS ballot' or msg == 'Move ISO 10303-17 from SDT 24 to SDT 36' or msg == 'Request 9-month extension for ISO 10303-209 ed3' or msg == 'Approval to use Jira/Git procedure for select projects' or msg == 'Approve draft for CIB ballot of JWG 24 procedure' or msg == 'To establish a reduced ballot period for New Work Item Proposals' or msg == 'Appointment of Convenors and Deputy Convenors' or msg == 'Place ISO 10303-209 ed3 on hold' or msg == 'Schedule Change for ISO/TS 23301' or msg == 'Create an Advisory Group on Core Terminology for industrial data' or msg == 'Extend term of the Ad Hoc Group 2 on Nuclear Digital Ecosystem Specification' or msg == 'Conduct a review of ISO/TC 184/SC 4 N1167 “SC4 Industrial Data Framework”' or msg == 'Launch combined NP/CD for ISO 10303-239 ed3' or msg == 'Establish an Ad Hoc Group on UUID management for industrial data' or msg == 'Update the SC 4 Handbook to incorporate standing documents' or msg == 'ISO 8000-2 Vocabulary for the ISO 8000 series Living Lab' or msg == 'ISO 15926-4 Uniform Resource Identifiers Living Lab':
                continue 
            elif 'Appointment of ' in msg and len(msg) < 50:
                continue
                
            atype = act.get('type', 'resolves')
            
            clean_msg = clean_text(msg)
            if not clean_msg: continue
            
            if is_acclamation(atype, clean_msg):
                acclaim_id = f"{year_month}-acclaim-{acclaim_idx:02d}"
                title = get_acclaim_title(clean_msg)
                
                acclaim_res = {
                    'identifier': acclaim_id,
                    'subject': res.get('subject', 'ISO/TC 184/SC 4 "Industrial data"'),
                    'title': title,
                    'dates': res.get('dates', []),
                    'actions': [
                        {
                            'type': 'thanks',
                            'message': LiteralScalarString(clean_msg),
                            'dates': act.get('dates', res.get('dates', []))
                        }
                    ]
                }
                new_resolutions.append(('acclaim', acclaim_res))
                acclaim_idx += 1
                continue
                
            lower_msg = clean_msg.lower()
            if lower_msg.startswith('noting') or lower_msg.startswith('recalling') or lower_msg.startswith('recognizing') or lower_msg.startswith('recognising'):
                ctype = 'noting'
                if lower_msg.startswith('recalling'): ctype = 'recalling'
                elif lower_msg.startswith('recognizing'): ctype = 'recognizing'
                elif lower_msg.startswith('recognising'): ctype = 'recognises'
                
                res['considerations'].append({
                    'type': ctype,
                    'message': LiteralScalarString(clean_msg),
                    'dates': act.get('dates', res.get('dates', []))
                })
                continue
                
            # verbs
            if 'requests' in lower_msg and atype == 'resolves': atype = 'requests'
            elif 'appoints' in lower_msg and atype == 'resolves': atype = 'appoints'
            elif 'instructs' in lower_msg and atype == 'resolves': atype = 'instructs'
            elif 'creates' in lower_msg and atype == 'resolves': atype = 'creates'
            elif 'establishes' in lower_msg and atype == 'resolves': atype = 'establishes'
            elif 'approves' in lower_msg and atype == 'resolves': atype = 'approves'
            elif 'cancels' in lower_msg and atype == 'resolves': atype = 'decides'
            elif 'nominates' in lower_msg and atype == 'resolves': atype = 'nominates'
            elif 'invites' in lower_msg and atype == 'resolves': atype = 'asks'
            elif 'extends' in lower_msg and atype == 'resolves': atype = 'decides'
            elif 'accepts' in lower_msg and atype == 'resolves': atype = 'accepts'
            
            if atype not in ['accepts', 'acknowledges', 'adoption', 'adopts', 'agrees', 'allocates', 'appoints', 'appreciates', 'appreciation', 'approves', 'asks', 'assigns', 'chairs', 'communicating', 'confirms', 'considers', 'consults', 'creates', 'decides', 'defines', 'delegates', 'delivering', 'directs', 'disbands', 'drafting', 'elects', 'empowers', 'encourages', 'endorses', 'estabilishes', 'establishes', 'gathering', 'identifies', 'instructs', 'investigates', 'nominates', 'notes', 'notifies', 'recognises', 'recognizes', 'reminds', 'recommends', 'registers', 'regrets', 'request', 'replaces', 'requests', 'resolves', 'restates', 'scopes', 'secures', 'sends', 'supports', 'thanks', 'welcomes', 'withdraws', 'unanimous', 'majority', 'minority']:
                atype = 'resolves'
                
            new_actions.append({
                'type': atype,
                'message': LiteralScalarString(clean_msg),
                'dates': act.get('dates', res.get('dates', []))
            })
            
        if 'considerations' in res:
            for cons in res['considerations']:
                if 'message' in cons and not isinstance(cons['message'], LiteralScalarString):
                    cons['message'] = LiteralScalarString(clean_text(cons['message']))
                    
        if new_actions:
            res['actions'] = new_actions
            if not res['considerations']:
                del res['considerations']
            new_resolutions.append(('normal', res))

    final_res = []
    acclaims = []
    for t, r in new_resolutions:
        if t == 'normal':
            final_res.append(r)
        else:
            acclaims.append(r)
    
    data['resolutions'] = final_res + acclaims
    
    with open(filepath, 'w') as f:
        yaml.dump(data, f)
        
    print(f"Processed {filepath}")

process_file("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2019-11-marina-del-rey-usa.yaml", "201911")
process_file("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2020-05-virtual.yaml", "202005")
process_file("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2020-11-virtual.yaml", "202011")
process_file("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2021-05-virtual.yaml", "202105")
