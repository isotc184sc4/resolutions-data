import yaml
import re

# 1. 2006-03
yaml_content_1 = """metadata:
  title: Resolutions of the plenary meeting of ISO/TC 184/SC 4, Vico Equense, Italy, March 5, 2006 -- March 10, 2006
  dates:
  - start: '2006-03-05'
    end: '2006-03-10'
    kind: meeting
  source: ISO/TC 184/SC 4 Secretariat
  venue: Vico Equense, Italy
resolutions:
- identifier: '664'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Approval of Project Leaders and Project Editors for SC 4 Projects
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: approves
    message: |
      SC 4 approves the following new project leaders or project editors for the associated SC 4 projects:

      |===
      |Project |Leader |Editor

      |ISO 10303-0224 ed3 |Len Slovensky |
      |===
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '665'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Reappointment of WG 3 Deputy Convenor
  dates:
  - start: '2006-03-15'
    kind: decision
  considerations:
  - type: noting
    message: |
      SC 4 appreciates and accepts the offer of Len Slovensky to serve as Deputy Convenor of WG 3.
    dates:
    - start: '2006-03-15'
      kind: effective
  actions:
  - type: approves
    message: |
      SC 4 approves the nomination of Len Slovensky to serve for an additional three year term.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '666'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Reappointment of JWG 8 Convenor
  dates:
  - start: '2006-03-15'
    kind: decision
  considerations:
  - type: noting
    message: |
      SC 4 appreciates and accepts the offer of Jean-Jacques Michel to serve as Convenor of JWG 8.
    dates:
    - start: '2006-03-15'
      kind: effective
  actions:
  - type: approves
    message: |
      SC 4 approves the nomination of Jean-Jacques Michel to serve for an additional three year term.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '667'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Reappointment of WG 12 Convenor
  dates:
  - start: '2006-03-15'
    kind: decision
  considerations:
  - type: noting
    message: |
      SC 4 appreciates and accepts the offer of Keith Hunten to serve as Convenor of WG 12.
    dates:
    - start: '2006-03-15'
      kind: effective
  actions:
  - type: approves
    message: |
      SC 4 approves the nomination of Keith Hunten to serve for an additional three year term.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '668'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Request active liaison with ISO/TC 229 and appoint liaison officers
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: requests
    message: |
      SC 4 requests an active two-way liaison with ISO/TC 229, Nanotechnology, and requests the SC 4 Secretary to confirm these liaisons with the ISO Central Secretariat.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: appoints
    message: |
      SC 4 appoints Ms Nonna Bond and Dr. Lars Ericson as the liaison officers from SC 4 to ISO/TC 229.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: requests
    message: |
      The SC 4 Secretary is also requested to solicit additional nominations from the ISO/TC 184/SC 4 P-members.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '669'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Launch AP 203 ed 2 DIS ballot and register New Work Item
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: accepts
    message: |
      SC 4 accepts the proposal of the AP 203 ed2 project team to launch a DIS ballot on the revised Technical Specification ISO/TS 10303-203, and requests its Secretariat to register the necessary New Work Item with ISO.

      Referenced documents: See WG 2N1591 -- issues log for AP203 and WG 12N3277 issues log for GD&T modules for additional information.

      Action item: Secretariat to request the AP203 ed2 team to confirm that they will use the current part 10303-55 and the revised 10303-111, currently under DIS ballot, to support construction history, prior to submitting the DIS ballot for AP203 ed2.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '670'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Register New Work Items for ISO 10303-52, 10303-53, and 10303-110
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: requests
    message: |
      SC 4 requests its Secretariat to register the necessary New Work Items for 10303-52, 10303-53, and 10303-110 with ISO, in order to allow them to proceed to DIS ballot.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '671'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Assign ISO 8000 to WG 12 temporarily
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: assigns
    message: |
      SC 4 assigns the current project ISO 8000 -- (Catalogue Management Systems - Requirements) to its Working Group 12 on a temporary basis until the establishment of a new Working Group 13 for Industrial Data Quality.

      Action to Secretariat: Secretariat is asked to inform the National Member Bodies of the new project and request them to nominate experts to the project.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '672'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Extend New Work Item Ballot for AP241
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: resolves
    message: |
      Based on the comments from IAI and SC 4 members, SC 4, as an exception, extends the ballot closing date for the New Work Item proposal on Generic Model for Life Cycle Support of AEC Facilities until July 31, 2006.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: encourages
    message: |
      SC 4 encourages IAI and WG 3 Teams 8, 22, and 23 to refine the NWI proposal so that it is mutually acceptable.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '673'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Invite host organizations to organize industry sector themes for meetings
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: asks
    message: |
      SC 4 invites host organizations to work with the International Industry STEP Centers and the SC 4 Chairman and Secretariat to organize industry sector themes for SC 4 meetings as appropriate, which may be reflected in the content of OTF, Liaison Plenary, training, tutorials and Implementation activities.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '674'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Express interest in taking responsibility for RFID standards and appoint delegates
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: resolves
    message: |
      SC 4 expresses its interest in taking responsibility for Industrial Data application standards for radio frequency identifiers (RFIDs), in cooperation with ISO/IEC JTC 1/SC 31.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: appoints
    message: |
      SC 4 appoints the following as delegates to attend the meeting of the joint ad hoc group to consider how to take ISO 21849 forward to multiple industries to be held in Lawrenceville, NJ, USA, 2006-04-11/12.

      * King Yee
      * Gerald Radack
      * Peter Benson
      * Nils Sandsmark
      * David Leal
      * Norman Swindells
      * Howard Mason
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: requests
    message: |
      SC 4 requests the delegation to provide a written report within two weeks of the meeting, and an oral report at the next SC 4 meeting.

      Note: Resolution amended by RESOLUTION 688 (Toulouse, France - June 2006).
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '675'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Submit Technical Corrigenda for STEP modules for publication
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: requests
    message: |
      SC 4 requests its Secretariat to submit the Technical Corrigenda for the following STEP modules to ISO for publication as second editions.

      ISO/TS 10303-1103, 1104, 1108, 1109, 1110, 1111, 1112, 1129, 1341, 1342, 1343, 1344, 1346, 1347, 1351, 1352
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '676'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Establish Working Group 13 on Industrial Data Quality
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: creates
    message: |
      SC 4 resolves to establish a new Working Group 13, Industrial Data Quality.

      The task of this working group will be to:

      * Establish a coherent definition of the structure of Quality Standards to be produced by SC 4, based on the results of the Product Data Quality Strategy meeting held on 2006-03-07 (SC 4 N2078)
      * Identify NWI and develop the necessary standards for accreditation of organizations and processes, and the quality criteria for information complying with each of the SC 4 standards, all to be published under the ISO 8000 series.
      * The current ISO 8000 work item will become part of the ISO 8000 series.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: requests
    message: |
      SC 4 requests its Secretariat to invite National Member Bodies to nominate experts and candidates for Convenorship for the group.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '677'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Participate in JWG with ISO/TC 171/SC 2 on PDF/E
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: resolves
    message: |
      SC 4 expresses its interest to participate in the proposed JWG with ISO/TC 171/SC 2 on PDF/E.
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: nominates
    message: |
      SC 4 nominates as participants:

      * Max Ungerer
      * Paul van Exel
    dates:
    - start: '2006-03-15'
      kind: effective
  - type: directs
    message: |
      SC 4 directs the delegation to provide written reports on progress with the project.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '678'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Invite submission of NWI for gear design data exchange
  dates:
  - start: '2006-03-15'
    kind: decision
  considerations:
  - type: noting
    message: |
      SC 4 welcomes the proposition from Germany to initiate a gear design project based upon the work in specification VDMA 23900.
    dates:
    - start: '2006-03-15'
      kind: effective
  actions:
  - type: asks
    message: |
      SC 4 invites them to submit any necessary NWI to SC 4 for consideration.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: '679'
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Appointment of QC Coordinator
  dates:
  - start: '2006-03-15'
    kind: decision
  considerations:
  - type: noting
    message: |
      SC 4 appreciates and accepts the offer of Peter Benson to serve as Quality Coordinator.
    dates:
    - start: '2006-03-15'
      kind: effective
  actions:
  - type: approves
    message: |
      SC 4 approves the nomination of Peter Benson to serve for a three year term.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: 200603-acclaim-01
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Thank SC 4 Liaisons and Plenary presenters
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: thanks
    message: |
      SC 4 appreciates our SC 4 Liaisons for their representation to and for ISO/TC 184/SC 4.

      A special thank you to the SC 4 Liaison Plenary presenters for their insightful and comprehensive presentations:

      |===
      |Organization |Presenter

      |ISO/TC 184 |Jean-Marc Chatelard
      |JWG 1 |Wolfgang Wilkes
      |OASIS |Mats Nilsson
      |ECCMA |Peter Benson
      |USPI-NL |Leo van Ruijven
      |ISO/TC 67 |Nils Sandsmark
      |ENEA |Anna Moreno
      |===
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: 200603-acclaim-02
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Thank ENEA and Oriente Hotel for hosting meeting
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: thanks
    message: |
      SC 4 wishes to give its unanimous thanks to ENEA, its Members and the staff of the Oriente Hotel for their efforts in organizing this meeting, arranging the facilities, excellent food, and excellent social events.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: 200603-acclaim-03
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Thank Dr. Anna Moreno and staff for meeting coordination
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: thanks
    message: |
      SC 4 expresses its particular thanks to Dr. Anna Moreno for providing the overall excellent coordination for the entire SC 4 Meeting in Vico Equense.

      SC 4 also wishes to recognize the members of her staff for their superior administrative support, outstanding hospitality, both before and during the ISO/TC 184/SC 4 meeting. They are; Mario Montanino, Anna Amato, Celestina Coccia, Augusto Massari, Enzo Moreno and Imma e Francesco Arpino.
    dates:
    - start: '2006-03-15'
      kind: effective

- identifier: 200603-acclaim-04
  subject: ISO/TC 184/SC 4 "Industrial data"
  title: Thank Rosaria Savarese
  dates:
  - start: '2006-03-15'
    kind: decision
  actions:
  - type: thanks
    message: |
      SC 4 expresses its particular thanks to Rosaria Savarese from the Town Hall for taking time to speak to the SC 4 members.
    dates:
    - start: '2006-03-15'
      kind: effective
"""
with open("/Users/mulgogi/src/isotc184sc4/resolutions/plenary/plenary-2006-03-vico-equense-italy.yaml", "w") as f:
    f.write(yaml_content_1)
print("Written 2006-03")
