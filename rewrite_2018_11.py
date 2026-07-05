import yaml

data = {
  'metadata': {
    'title': 'Resolutions of the plenary meeting of ISO/TC 184/SC 4, Chicago, United States, November 4, 2018 -- November 9, 2018',
    'dates': [{'start': '2018-11-04', 'end': '2018-11-09', 'kind': 'meeting'}],
    'source': 'ISO/TC 184/SC 4 Secretariat',
    'venue': 'Chicago, United States'
  },
  'resolutions': []
}

def add_res(res):
    data['resolutions'].append(res)

add_res({
    'identifier': '986',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Approve Project Leaders and Project Editors for SC 4 Projects',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'approves',
            'message': 'SC 4 approves the following Project Leaders and Project Editors for the associated Projects:\n\n|===\n|Project |Working Group |Project Leader/Editor\n\n|ISO 15926-10 |WG 3 |Leader: Paul Van Exel\n|ISO 15926-10 |WG 3 |Editors: Leo van Ruijven, Hiroshi Okada\n|ISO 15926-6ed2 |WG 3 |Leader: Paul Van Exel\n|ISO 10303-1 |WG 12 |Leader: Keith Hunten\n|===\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '987',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Reappoint Martin Hardwick and Bengt Olsson as WG 15 Convenors',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'appoints',
            'message': 'SC 4 appoints Martin Hardwick as Convenor and Bengt Olsson as Deputy Convenor for the WG 15 "Digital Manufacturing" for a further three year term, with appreciation for their offers to serve in those capacities.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '988',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Reappoint Nils Sandsmark as WG 22 Convenor',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'appoints',
            'message': 'SC 4 appoints Nils Sandsmark as Convenor for the WG 22, "Reference data validation team" for a further three year term, with appreciation for his offer to serve in that capacity.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '989',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Appoint Tim King as WG 23 Convenor',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'acknowledges',
            'message': 'SC 4 expresses its appreciation and gratitude to Aminata Mbengue for her service as Convenor of WG 23 since its inception and wishes her all success in future endeavours.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'appoints',
            'message': 'SC 4 appoints Tim King as Convenor for the WG 23 "Vocabulary validation team" for a three year term, with appreciation for his offer to serve in that capacity.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '990',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Move ISO 10303-238ed2 to 48-month development track',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to move the ISO 10303-238ed2 project from 36 months to the 48 month development track.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '991',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Remove ISO 8000-3 from the ISO work programme',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'decides',
            'message': 'SC 4 cancels the project 60784 for ISO/NP TS 8000-3.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '992',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Correct title of ISO 8000-116',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'approves',
            'message': 'SC 4 approves change of the title "Data quality -- Part 116: Application of ISO 8000-115 to the formatting of Authoritative Legal Entity Identifiers (ALEI) for individuals and organizations" to "Data quality -- Part 116: Master data: Exchange of quality identifiers: Application of ISO 8000-115 to authoritative legal entity identifiers" and requests its Secretariat to contact ISO CS to update the ISO work programme.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '993',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Apply 8-week ballot duration to NP for 8000-81',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to apply the 8 week ballot duration to the NP for 8000-81, Data quality assessment based on data profiling.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '994',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Apply 8-week ballot duration to NP for 10303-59ed3',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to apply the 8 week ballot duration to the NP for 10303-59ed3, Integrated generic resource: Quality of product shape data.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '995',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Apply 8-week ballot duration to future NP for 14306ed3',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to apply the 8 week ballot duration to the future NP for 14306ed3, JT file format specification for 3D visualization following a successful review by JWG 16 for scope per action item 195 from the Secretariat.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '996',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Apply 8-week ballot duration to NPs for 10303 parts',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to apply the 8 week ballot duration to the following NPs for 10303:\n\n* 10303-15 (SysML XMI to XSD binding)\n* 10303-16 (SysML XMI to EXPRESS binding)\n* 10303-17 (EXPRESS to SysML XMI binding)\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '997',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Establish PWI for Industrial Requirements for Product Data Visualization',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'resolves',
            'message': 'SC 4 launches a PWI to update its requirements for visualization and to create a Technical Report on "Industrial Requirements for Product Data Visualization".\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to invite member bodies to nominate experts to JWG 16 to undertake this preliminary work.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '998',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Submit Quality Information Framework for fast track ballot',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to submit QIF 3.0, together with its harvesting explanatory report and the mapping between STEP and QIF MBD for DIS ballot under the fast track procedure.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '999',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Agree on path forward for Edition 2 of ISO 10303-242',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'agrees',
            'message': 'SC 4 agrees that the following points specified by WG 12 for the way forward with AP 242ed2 DIS and the extended architecture specification shall be used as a basis for the second AP 242ed2 DIS ballot:\n\n1. Agreement to retain ISO/TS 10303-4442 in the standard\n2. Agreement to continue to provide an EXPRESS representation for the Integrated Resources, AIM, ARM and Domain Model\n3. Agreement to retain EXPRESS\n4. Agreement to use SysML as the modelling language for AP 242ed2 domain model in ISO/TS 10303-4442\n5. Agreement to re-ballot the standing documents N3210, N3211, and N3212 with a revision to focus the documents only on the specific materials required to support AP 242ed2 and ISO/TS 10303-4442. All materials that speak to the future state of the extended architecture will be moved to a technical report and addressed by an ad hoc group on the strategy for extended architecture with Allison Barnard Feeney as chief editor\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'asks',
            'message': 'SC 4 invites members from each NSB to join and contribute to the refinement of the content.\n\n6. Agreement to create SMRL V8 with the required updates that support AP 242ed2.\n7. Agreement to create one or more NPs that address the implementation of SysML as a modelling solution into the internal procedures of SC 4. This work will primarily impact WG 11 and coordination has taken place at the Chicago meeting to define the work required by WG 11.\n8. Acknowledgement that the strategy for extended architecture contained in the technical report will require further action by the ad hoc group as there exists a strong dependency between the strategy and the implementation of follow on capabilities for AP 239ed3 and AP 243.\n9. Acknowledgement that future releases of extended architecture capabilities will require update and revision of the standing documents noted. These standing documents shall be balloted incrementally as changes are declared.\n10. Acknowledgement that the current priority is to resolve documented comments against the ballot content for AP 242ed2. Any discovery or comments not formally declared will be noted as a bug in the bug tracking system against a future edition.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '1000',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Transfer ISO 22745 and ISO 29002 to WG 13',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'requests',
            'message': 'SC 4 requests its Secretariat to coordinate with ISO/CS and transfer ISO 22745 and ISO 29002 and all their parts from WG 2 to WG 13.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'welcomes',
            'message': 'SC 4 welcomes the interest of IEC SC3D in the joint development of the new edition of ISO 29002, and requests its Secretariat to reactivate its existing liaison to TC 3 to include SC3D.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '1001',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Disband WG 2 and assign ISO 13584 to JWG 24',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'assigns',
            'message': 'SC 4 assigns ISO 13584 to JWG 24.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'disbands',
            'message': 'SC 4 disbands WG 2, thanking its experts for their contribution.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        },
        {
            'type': 'requests',
            'message': 'SC 4 requests the IEC SC 3D to concur.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '201811-acclaim-01',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Thank SC 4 Liaisons and presenters',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'thanks',
            'message': 'SC 4 expresses its appreciation to our SC 4 Liaisons and the presentations that were provided:\n\n* TC 68/SC 8 (LEI) and ECCMA, Peter Benson\n* TC 171/SC 2, Kenny Swope\n* JTC 1/SC 24 and Web3D Consortium, Christophe Mouton\n* Energistics, Jay Hollingsworth\n* TC 37/SC 3, Written Report Submitted\n* TC 59/SC 13, Written Report Submitted\n* TC 67, Written Report Submitted\n* ISO/TC 172/SC 1, Written Report Submitted\n* TC 251, Written Report Submitted\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '201811-acclaim-02',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Thank Open Technical Forum presenters',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'thanks',
            'message': 'SC 4 expresses its appreciation to the following individuals and organizations for their participation in the 76th ISO/TC 184/SC 4 Open Technical Forum in Chicago, IL USA 2018-11-05:\n\n* ISO 8000-2, Tim King\n* Extended Architecture, Jean Brange\n* ISO 15926, Lillian Hella\n* PLCS Library, Jonas Rosen\n* ISO 10303 & StepMod, Keith Hunten\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '201811-acclaim-03',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Thank Industry Day participants',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'thanks',
            'message': 'SC 4 expresses its appreciation to the following individuals and organizations for their participation in the 76th ISO/TC 184/SC 4 Industry Day in Chicago, IL USA 2018-11-05:\n\n* Jiwan Hayre, Boeing\n* Kenny Swope, Boeing\n* Bob Deragish, Parker Aerospace\n* Martin Hardwick, StepTools\n* Jochen Haenisch, Jotne\n* Moneer Helu, NIST\n* Curtis Brown, DMSC/QIF\n* Chris Johnson, Lockheed Martin\n* Peter Benson, ECCMA\n* Tim King, Babcock International\n* Ashutosh Agarwal, Uptake\n* Dan Carnahan\n* Peter Eales, MRO Insyte\n* Van Bicknell\n* Daryl Crockett, ValidDatum\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})

add_res({
    'identifier': '201811-acclaim-04',
    'subject': 'ISO/TC 184/SC 4 "Industrial data"',
    'title': 'Thank Chicago meeting hosts and staff',
    'dates': [{'start': '2018-11-15', 'kind': 'decision'}],
    'actions': [
        {
            'type': 'thanks',
            'message': 'SC 4 expresses its appreciation to Peter Benson, Brandi Fisher, and the rest of ECCMA\'s staff for hosting the 76th ISO/TC 184/SC 4 Plenary in Chicago, IL USA during 2018-11-05/09. Special acknowledgement is extended to UI Labs and its staff for their seamless and attentive support throughout the week.\n',
            'dates': [{'start': '2018-11-15', 'kind': 'effective'}]
        }
    ]
})


class CustomDumper(yaml.Dumper):
    def represent_scalar(self, tag, value, style=None):
        if tag == 'tag:yaml.org,2002:str' and '\n' in value:
            style = '|'
        return super().represent_scalar(tag, value, style)

with open('plenary/plenary-2018-11-chicago-usa.yaml', 'w') as f:
    yaml.dump(data, f, Dumper=CustomDumper, sort_keys=False, allow_unicode=True, width=1000)

