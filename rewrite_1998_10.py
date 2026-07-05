import yaml
import re

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1998-10-beijing-china.yaml", "r") as f:
    data = yaml.safe_load(f)

# Hardcode the rewriting of messages since there are only 10 resolutions
new_resolutions = []
for res in data['resolutions']:
    res_id = res['identifier']
    new_res = {
        'identifier': res_id,
        'subject': res['subject'],
        'title': '',
        'dates': res.get('dates', [])
    }
    
    if res_id == '379':
        new_res['title'] = 'Approve new project leaders and project editors'
        new_res['actions'] = [{
            'type': 'approves',
            'message': '''SC 4 approves the following new project leaders or project editors for the associated SC 4 projects:

|===
| ISO Project # | Project Lead | Document Editor

| ISO 10303-43e2 | Julian Fowler | Julian Fowler
| ISO 10303-209 | Adnan Yucel |
| ISO 10303-224 | Len Slovensky | Len Slovensky
| ISO 10303-314 | Manfred Fischer | Manfred Fischer
| ISO 10303-324 | Len Slovensky | Len Slovensky
| ISO 10303-504 | Bill Anderson |
| ISO 10303-505 | Bill Anderson |
| ISO 10303-506 | Bill Anderson |
| ISO 10303-507 | Jochen Haenisch |
| ISO 10303-508 | Jochen Haenisch |
| ISO 10303-509 | Jochen Haenisch |
| ISO 10303-517 | Martin Philipp |
| ISO 10303-519 | Martin Philipp |
| ISO 10303-520 | Martin Philipp |
| ISO 13584-1 | Ekkehard Zwicker | Robert Schuler
| ISO 13584-10 | Ekkehard Zwicker |
| ISO 13584-24 | Eric Sardet |
| ISO 13584-26 | Gerry Radack | Gerry Radack
| ISO 13584-31 | Gerd Ehinger | Ben Kassel
|===\n''',
            'dates': [{'start': '1998-10-15', 'kind': 'effective'}]
        }]
    elif res_id == '380':
        new_res['title'] = 'Request ability to maintain previous editions of SC 4 standard parts'
        new_res['actions'] = [
            {'type': 'agrees', 'message': 'SC 4 agrees that the ability to maintain a previous edition of a part when a new edition is published may be useful in managing the evolution of SC 4 Standards.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]},
            {'type': 'agrees', 'message': 'SC 4 further agrees that the decision to exercise this ability should be made on a part-by-part basis.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]},
            {'type': 'requests', 'message': 'SC 4 requests its Secretariat to request a waiver from ISO Central Secretariat which would enable the ability to retain up to two editions of a part, to inquire as to what guidelines should apply, and to present an appropriate procedure for ratification at the next SC 4 meeting.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}
        ]
    elif res_id == '381':
        new_res['title'] = 'Approve appointment of Matthew West as Deputy Convener of WG 10'
        new_res['actions'] = [{'type': 'approves', 'message': 'SC 4 approves the appointment of Matthew West as Deputy Convener of ISO/TC 184/SC 4/WG 10.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
    elif res_id == '382':
        new_res['title'] = 'Establish active two-way liaison with NAFEMS'
        new_res['actions'] = [
            {'type': 'requests', 'message': 'SC 4 requests an active two-way liaison with NAFEMS, and requests the SC 4 Secretary to confirm this liaison with the ISO Central Secretariat.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]},
            {'type': 'approves', 'message': "SC 4 approves David Leal as the person to liaise with NAFEMS on SC 4's behalf.\n", 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}
        ]
    elif res_id == '383':
        new_res['title'] = 'Establish JWG 14 with ISO/TC 8/SC 10 for Ship Operational Logs'
        new_res['considerations'] = [
            {'type': 'noting', 'message': 'Noting the approval of the NWI "Ship Operational Logs, Records, and Messages" as ISO 10303-234.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]},
            {'type': 'recognizing', 'message': 'Recognizing that the information requirements are derived in part from the scope of ISO/TC 8/SC 10, Ships and Marine Technology/Computer Applications.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}
        ]
        new_res['actions'] = [
            {'type': 'approves', 'message': 'SC 4 approves the creation of a joint working group (JWG) between ISO/TC 8/SC 10 and ISO/TC 184/SC 4.\n\nThe scope of the JWG shall be the development of Application Protocol ISO 10303-234 including documentation that supports the usage of this AP.\n\nIn order to ensure a development in accordance with the STEP procedures for Application Protocols and harmonisation with the current ship APs the joint working group shall be placed as JWG 14, "Ship Operational Logs", under ISO/TC 184/SC 4. To draw maximum benefit from the expertise of ISO/TC 8/SC 10, SC 4 encourages the active participation of ISO/TC 8/SC 10 experts in the JWG. The JWG shall collaborate closely with ISO/TC 184/SC 4/WG 3/T23 Ships, ISO/TC 8/WG 6, Maritime Navigation and Radio Communication Equipment and Systems / Digital Interfaces for Navigational Equipment within a Ship, and IEC/TC 18, Electrical Installations of Ships and of mobile and fixed Offshore Units.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}
        ]
    elif res_id == '384':
        new_res['title'] = 'Disband WG 6 and transfer residual work to WG 11'
        new_res['actions'] = [{'type': 'resolves', 'message': 'SC 4 resolves to disband its working group 6, noting that any residual work is transferred to WG 11.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
    elif res_id == '385':
        new_res['title'] = 'Distribute capability definition for 2003 release and request comments'
        new_res['considerations'] = [{'type': 'following', 'message': 'Further to Resolution 376.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
        new_res['actions'] = [{'type': 'requests', 'message': 'SC 4 requests its Secretariat to distribute the attached outline capability definition for the April 2003 release of SC 4 standards (SC 4 N776) to P and O-members and liaisons, with an invitation to provide written comments by the end of 1998, and further to nominate experts for an ad hoc meeting to refine the definition, to be held during the January 1999 meeting of SC 4.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
    elif res_id == '386':
        new_res['title'] = 'Announce meeting on collaborative use of geometry with ISO/TC 211'
        new_res['considerations'] = [{'type': 'noting', 'message': 'Noting that ISO/TC 184/SC 4 is pleased to see that ISO/TC 211 is ready to harmonize its geometry representation with the one published in ISO 10303-42 and ISO 10303-43, as indicated by ISO/TC 211 Resolution 78.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
        new_res['actions'] = [
            {'type': 'instructs', 'message': 'ISO/TC 184/SC 4 instructs its secretariat to announce a meeting on collaborative use of geometry between ISO 10303-42/43 and ISO 15046-7/11, to be held 1999-02-01/05 in the USA.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]},
            {'type': 'encourages', 'message': 'ISO/TC 184/SC 4 encourages all its working groups and projects and requests especially the Shape Representation project in its WG 12 and the Building and Construction Team in its WG 3 to participate in this meeting.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}
        ]
    elif res_id == '387':
        new_res['title'] = 'Approve WG 8 request for re-initialization of time schedule for MANDATE'
        new_res['actions'] = [{'type': 'approves', 'message': 'SC 4 approves the WG 8 request for a re-initialization of its time schedule for MANDATE based on the proposal of the WG 8 September 1998 slippage report (ISO/TC 184/SC 4/WG 8 N190) and the ISO directives.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]
    elif res_id == '388':
        new_res['title'] = 'Thank Chinese hosts for the SC 4 meeting in Beijing'
        new_res['actions'] = [{'type': 'thanks', 'message': 'SC 4 wishes to thank the China State Bureau of Quality and Technical Supervision, the China Standardization and Information Classifying and Coding Institute, the China STEP Center, and Mr. Ping Wang and his staff for their great hospitality, graciousness, and high quality of service in hosting the SC 4/WGs Meeting in Beijing, China, 1998-10-05/09.\n', 'dates': [{'start': '1998-10-15', 'kind': 'effective'}]}]

    new_resolutions.append(new_res)

data['resolutions'] = new_resolutions

class LiteralString(str):
    pass

def literal_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(LiteralString, literal_presenter)

for res in data['resolutions']:
    for act in res.get('actions', []):
        act['message'] = LiteralString(act['message'])
    for cons in res.get('considerations', []):
        cons['message'] = LiteralString(cons['message'])

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1998-10-beijing-china.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)

