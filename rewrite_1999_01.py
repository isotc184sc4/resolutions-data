import yaml
import re

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1999-01-san-francisco-ca-usa.yaml", "r") as f:
    data = yaml.safe_load(f)

new_resolutions = []
for res in data['resolutions']:
    res_id = res['identifier']
    new_res = {
        'identifier': res_id,
        'subject': res['subject'],
        'title': '',
        'dates': res.get('dates', [])
    }
    
    if res_id == '389':
        new_res['title'] = 'Approve new project leaders and project editors'
        new_res['actions'] = [{
            'type': 'approves',
            'message': '''SC 4 approves the following new project leaders or project editors for the associated SC 4 projects:

|===
| ISO Project # | Project Lead | Document Editor

| 10303-208 | Janice Chinn, Tim Turner | John Kendall
|===\n''',
            'dates': [{'start': '1999-01-15', 'kind': 'effective'}]
        }]
    elif res_id == '390':
        new_res['title'] = 'Direct Secretariat to provide ballot documents in electronic format'
        new_res['actions'] = [
            {'type': 'directs', 'message': 'SC 4 directs its Secretariat to provide SC 4 ballot documents to P-members, O-members and A-liaisons in electronic format as follows:\n\n* SC 4 ballot documents will be made available on SOLIS in their original format, PDF and ASCII text.\n\n* SC 4 ballots will be posted to SOLIS, and announced via the SC 4 and P-Member exploder two weeks prior to the official start date of the ballot.\n\n* Paper copies of SC 4 ballot documents will be provided to P-members on a per-request basis only\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'directs', 'message': 'SC 4 directs the secretariat to deliver an annex to the handbook detailing this process by April 9 1999.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '391':
        new_res['title'] = 'Amend SC 4 Organization Handbook procedures for handbook changes'
        new_res['considerations'] = [{'type': 'recognizing', 'message': 'Recognizing that the version of the SC 4 Organization Handbook held on SOLIS is the master copy of the document.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
        new_res['actions'] = [{'type': 'resolves', 'message': 'SC 4 amends the approval procedure for changes as follows (changes highlighted):\n\n5.7.5.2 Approval of the Minutes and Handbook Changes of the Preceding Meeting\nApproval of the minutes of the preceding meeting confirms that resolutions appearing in the minutes properly reflect all the editorial changes made during the meeting. If resolutions caused changes in the SC 4 Organization Handbook, the proper inclusion and publication of those changes on SOLIS shall be separately confirmed.\n\n5.11 Updates to the ISO/TC 184/SC 4 Organization Handbook\nUpdates to the ISO/TC 184/SC 4 Organization Handbook for changes to the organization or the procedures require a regular resolution paper (see 5.7.3.1). The resolution paper must contain the exact wording of the text to be included or changed in the SC 4 Organization Handbook. Changes to the SC 4 Organization Handbook take effect immediately after their decision in the SC 4 Meeting. While the minutes of the meeting report the outcome of the decision, the amended form of the Handbook will be published on SOLIS for confirmation at the next SC 4 Meeting. Because frequent changes can be expected in the Appendices, changes will be made at the discretion of the Secretariat, published on SOLIS and distributed at the next SC 4 meeting.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '392':
        new_res['title'] = 'Amend SC 4 Organization Handbook to permit discussion of position papers'
        new_res['actions'] = [{'type': 'approves', 'message': 'SC 4 approves the following amendment to the Organisation Handbook to permit the discussion of position papers at SC 4 meetings (changes highlighted):\n\n5.7.1 Calling an SC 4 Meeting\nSC 4 meeting dates and locations shall be published at least 18 months ahead in order to allow member bodies to plan national meetings and travel budgets. An SC 4 meeting is officially called by transmitting the invitation to the meeting and the agenda at least four months prior to the date of the meeting. A shorter period is permissible if no P-member objects. Update pages to the SC 4 Organization Handbook, ordinary resolutions, position papers and papers for decision shall be mailed at least six weeks prior to the date of the meeting (IDP1, 3).\n\n5.7.2 SC 4 Meeting Agenda\nThe SC 4 Meeting Agenda follows a general sequence, in which a number of items are prescribed.\nThe content of the Agenda is the following:\n1. Opening of the Meeting\n2. Roll Call of Delegates\n3. Appointment of Drafting Committee and of two vote tellers\n4. Adoption of the Agenda\n5. Minutes and Handbook Changes of the Preceding Meeting\n6. Administrative Reports\n   6.1 Report of the Secretariat\n   6.2 Report from Liaisons\n7. Committee and WG reports\n   7.1 Reports from WG Conveners and Project Leaders\n   7.2 Reports from Quality Committee\n   7.3 Report from the PPC\n   7.4 Reports from Ad hoc Committees\n8. Resolution Papers\n   8.1 Ordinary Resolution Papers\n   8.2 Last-Day Resolution Papers\n   8.3 Position Papers for discussion\n9. Approving Conveners\n10. Future Meetings\n11. Closing the Meeting\n\n5.7.3 Adding Items to the Agenda\nThe Chairman of SC 4, the SC 4 Secretary, the P-members, and the Conveners of all Committees and WGs can add items to the agenda by submitting resolution papers and position papers for discussion.\n* Resolution papers shall contain background information stating the reasons for the resolution, the aims envisaged and the text of the resolution. Resolutions shall be carefully worded in order to achieve maximum clarity. See Annex G.3 for the format of a resolution paper.\n* Position papers shall contain background information for a particular issue, to permit an informed discussion at an SC 4 meeting and to allow the creation of a resolution on any consensus that may result from the discussion.\n\n5.7.3.1 Issuing a Resolution Paper\nAll resolution papers define a specific action, which may include a change to the organization or the procedures in the SC 4 Organization Handbook (see 5.11). Ordinary resolution papers, together with the agenda, must be available to P-members at least six weeks prior to the SC 4 Meeting. They must, therefore, be in the hands of the SC 4 Secretariat at least eight weeks prior to the SC 4 Meeting.\n\n5.7.3.2 Issuing a Last-Day Resolution Paper\nLast-day resolution papers may address urgent issues resulting from immediately preceding WG meetings for which a high level of acceptance may be expected. Last-day resolution papers cannot cause changes to the Organization Handbook, however, a temporary action may be initiated, which may lead to a regular resolution paper in a subsequent meeting. Copies of last-day resolution papers must be handed to the SC 4 Secretary or meeting desk by 10.30 in order to be available for pick-up by delegation leaders at 15.30 on the day preceding the start of the SC 4 meeting. A camera-ready hard copy and digital ASCII file shall be provided by the originating national body or convener.\nA last-day resolution will not be considered at the meeting if an objection is raised by a P-member. The resolution will be circulated as a letter ballot.\n\n5.7.3.3 Issuing a Position Paper\nPosition papers provide the background information for the discussion of an issue at the SC 4 meeting. They should clearly identify the issue and its implications, together with any other relevant information for the discussion. Position papers should be available to P-members at least six weeks prior to the SC 4 Meeting. They must, therefore, be in the hands of the SC 4 Secretariat at least eight weeks prior to the SC 4 Meeting.\nPosition papers submitted after this deadline must be handed to the SC 4 Secretary or meeting desk by 10.30 in order to be available for pick-up by delegation leaders at 15.30 on the day preceding the start of the SC 4 meeting. A camera-ready hard copy and digital ASCII file shall be provided by the originating national body or convener.\nSuch a position paper will not be considered at the meeting if an objection is raised by a P-member.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '393':
        new_res['title'] = 'Adopt SC 4N777 as strategic plan'
        new_res['actions'] = [
            {'type': 'adopts', 'message': 'SC 4 adopts SC 4N777 as its strategic plan and requests the Secretariat to publish the document on SOLIS, and forward it to the ISO/TC 184 Secretariat.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'invites', 'message': 'SC 4 invites the WG and QC Conveners to review the proposed tactics against their current procedures, and to identify any discrepancies.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '394':
        new_res['title'] = 'Allow nominated STEP projects to adopt modular approach'
        new_res['considerations'] = [{'type': 'following', 'message': 'Further to Resolution 374.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
        new_res['actions'] = [
            {'type': 'resolves', 'message': 'SC 4 resolves to allow nominated STEP projects to adopt the modular approach as defined in the following deliverables of the WG 10 STEP Modularization PWI:\n\n1. WG 10 N221 Guidelines for the content of application modules Revision 0.6\n2. WG 10 N222 Guidelines for the content of application protocols using application modules Revision 0.6\n3. WG 10 N219 Industrial Framework Model Version 0.95\n4. WG 10 N223 Application Module Development Points within the Application Protocol Development Process Draft 0.1\n5. WG 10 N246 The Proposed Approach to STEP Modularization (Slide Presentation)\n6. WG 10 N247 WG 10 STEP Modularization PWI Proposal for Standardization of Modules and Extensions Draft 0.3 (Slide Presentation)\n7. WG 10 N226 WG 10 STEP Modularization PWI Proposal for Standardization of Modules and Extensions Draft 0.1 (White Paper)\n8. WG 10 N227 WG 10 STEP Modularization Requirements Specification Revision 0.1\n9. WG 10 N228 STEP Modularization PWI Issue Log\n10. WG 10 N229 The STEP Modules Catalogue Demo\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'resolves', 'message': 'SC 4 resolves that the results of the nominated projects may be published as PASs or TSs.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'nominates', 'message': 'SC 4 nominates the Engineering Analysis Core Model and the PDES Inc modular extension projects to endeavor to develop their deliverables using the above process.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'directs', 'message': 'SC 4 directs the WG 10 STEP Modularization PWI to support these projects and continue the development of the required guidelines and processes until SC 4 approves the documents and the supporting SC 4 organizations are in place.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'requests', 'message': 'SC 4 requests that its members, liaisons and other organizations provide additional resources to support this effort in the following areas:\n\n11. finalizing requirements;\n12. resolving the remaining technical and organizational issues;\n13. reviewing and commenting on guideline documents;\n14. using the modular approach and providing feedback to WG 10;\n15. Addressing the use of ITAs, PASs and TSs within SC 4.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'requests', 'message': 'SC 4 requests WG 10 to report on progress on the pilot projects to the next SC 4 meeting.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '395':
        new_res['title'] = 'Establish Category A two-way liaison with Object Management Group'
        new_res['actions'] = [
            {'type': 'requests', 'message': 'SC 4 requests a Category A active two-way liaison with the Object Management Group, and requests that the SC 4 Secretary confirm this liaison with the ISO Central Secretariat.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'approves', 'message': 'SC 4 approves Peter Denno and Evan Wallace (both of NIST, U.S.) as the parties who will be responsible for maintaining this active liaison, with Evan Wallace designated the recipient for formal SC 4 mailings and other formal communications between SC 4 and the OMG.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '396':
        new_res['title'] = 'Modify SC 4 Handbook Section 5.7.3 to include A-liaisons'
        new_res['actions'] = [{'type': 'requests', 'message': 'SC 4 requests its Secretary to modify section 5.7.3 of the SC 4 Handbook to include A-liaisons in the list of organizations and individuals permitted to submit resolutions to SC 4.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '397':
        new_res['title'] = 'Accept A-liaison of IEC/TC 93 on JWG 9'
        new_res['actions'] = [
            {'type': 'accepts', 'message': 'SC 4 accepts the A-liaison of IEC/TC 93 on JWG 9.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'recommends', 'message': 'SC 4 recommends that JWG 9 prepare a plan by the Lillehammer meeting for increased co-operation with IEC/TC 93.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '398':
        new_res['title'] = 'Request ISO/TC 184 and ISO CS to provide a Technical Officer'
        new_res['considerations'] = [
            {'type': 'welcomes', 'message': 'SC 4 welcomes the nomination of a point of contact within the ISO CS, to work with the current IEC Technical Officer, noting that ISO/TC 184 is the only ISO Technical Committee with such an arrangement.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'noting', 'message': 'SC 4 notes the increasing importance of coordination with other ISO Technical Committees and Subcommittees, particularly in the context of the Memorandum of Understanding between ISO, IEC, UN/CEFACT and the participating International User Groups, and also seeks to fully exploit the new ISO deliverables and electronic publication methods.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
        new_res['actions'] = [{'type': 'requests', 'message': 'SC 4 requests ISO/TC 184 and the ISO CS to take the necessary steps to provide ISO/TC 184 with a Technical Officer from the ISO staff.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '399':
        new_res['title'] = 'Cancel projects 10303-222 and 10303-322 for composites'
        new_res['actions'] = [{'type': 'resolves', 'message': 'SC 4 resolves to cancel the following projects:\n\n* 10303-222 - Application Protocol: Exchange of product data for composites\n* 10303-322 - Abstract Test Suite: Exchange of product data for composites\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '400':
        new_res['title'] = 'Remove projects 10303-208/308 and 10303-222/322 from Release 2.0'
        new_res['actions'] = [{'type': 'resolves', 'message': 'SC 4 resolves to remove the following AP projects and their associated Abstract test suites from ISO 10303 release 2.0:\n\n* 10303-208/308 - Application Protocol: Lifecycle management - Change process\n* 10303-222/322 - Application Protocol: Exchange of product data for composites\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '401':
        new_res['title'] = 'Cancel project 10303-229/329 as NWI and approve as PWI'
        new_res['actions'] = [{'type': 'resolves', 'message': 'SC 4 cancels SC 4 project 10303-229/329 as New Work Item: "Application protocol: Exchange of design and manufacturing product information for forged parts"; but in recognition of the initiative\'s continued merit within SC 4, approves it as a preliminary work item, stage 0.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '402':
        new_res['title'] = 'Revise methods documents to allow use of SC 4 standards as Common Resources'
        new_res['actions'] = [
            {'type': 'requests', 'message': 'SC 4 requests QC to revise the SC 4 methods documents to allow the use of parts of other ISO/TC 184/ SC 4 standards as Common Resources in the development of STEP Application Interpreted Models, and other SC 4 standards.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]},
            {'type': 'requests', 'message': 'SC 4 requests WG 12 to develop procedures to enable and control the use of other ISO/TC 184/SC 4 parts as Common Resources in the development of STEP Application Interpreted Models, and other SC 4 standards.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}
        ]
    elif res_id == '403':
        new_res['title'] = 'Develop procedures to ensure EXPRESS models conform to ISO 10303-11'
        new_res['actions'] = [{'type': 'directs', 'message': 'SC 4 directs the Quality Committee and WG 11 to develop procedures to ensure that EXPRESS models in SC 4 standards conform to the requirements of ISO 10303-11 and to the guidelines for EXPRESS usage specified in the relevant methods documents.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]
    elif res_id == '404':
        new_res['title'] = 'Thank US PRO and Chuck Stark for hosting SC 4 meeting in San Francisco'
        new_res['actions'] = [{'type': 'thanks', 'message': 'SC 4 wishes to thank US PRO, Chuck Stark and his tireless support staff for their quality services and generous hospitality in hosting the SC 4/WGs meeting 1999-01-25/29.\n', 'dates': [{'start': '1999-01-15', 'kind': 'effective'}]}]

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

with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-1999-01-san-francisco-ca-usa.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)

