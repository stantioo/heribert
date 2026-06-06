# -*- coding: utf-8 -*-
import re, csv

# Raw lines from list_meetings (recorded_by = Tobias Koch), all 3 batches
RAW = r"""
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-06-05 | id: 152648476 | url: https://fathom.video/calls/698522900 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-06-05 | id: 152628140 | url: https://fathom.video/calls/698522896 | recorded by Tobias Koch
- 🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-06-05 | id: 152609691 | url: https://fathom.video/calls/698522892 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports <> Tobias Koch | 2026-06-05 | id: 152583490 | url: https://fathom.video/calls/698522904 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-06-05 | id: 152563775 | url: https://fathom.video/calls/698522899 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-06-05 | id: 152557585 | url: https://fathom.video/calls/698522905 | recorded by Tobias Koch
- 🎯 Check-In Call  Call | Nicholas Hennings <> Tobias Koch | 2026-06-05 | id: 152549535 | url: https://fathom.video/calls/698522898 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-06-03 | id: 151879035 | url: https://fathom.video/calls/695660290 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-06-03 | id: 151860977 | url: https://fathom.video/calls/695207807 | recorded by Tobias Koch
- 🛒 Sourcing Live-Call | Tobias Koch | 2026-06-03 | id: 151825661 | url: https://fathom.video/calls/695207804 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce <> Tobias Koch | 2026-06-03 | id: 151804165 | url: https://fathom.video/calls/695207800 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela <> Tobias Koch | 2026-06-03 | id: 151761427 | url: https://fathom.video/calls/695207801 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Tobias Koch | 2026-06-03 | id: 151747440 | url: https://fathom.video/calls/695207803 | recorded by Tobias Koch
- ⏰ Daily Office-Hour | Tobias Koch | 2026-06-02 | id: 151411152 | url: https://fathom.video/calls/693451578 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen <> Tobias Koch | 2026-06-02 | id: 151388600 | url: https://fathom.video/calls/693451575 | recorded by Tobias Koch
-  🎯 Check-In | GSP Operations <> ATLAS | 2026-06-02 | id: 151344604 | url: https://fathom.video/calls/693451579 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-06-02 | id: 151329303 | url: https://fathom.video/calls/693842989 | recorded by Tobias Koch
- 🎯 Check-In Call |  Sourcing & Einkauf: SaleLab GmbH <> ATLAS   | 2026-06-01 | id: 151039167 | url: https://fathom.video/calls/691489664 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi <> Tobias Koch | 2026-06-01 | id: 151021717 | url: https://fathom.video/calls/691489660 | recorded by Tobias Koch
- 🛒 Sourcing Live-Call | Tobias Koch | 2026-05-29 | id: 150607778 | url: https://fathom.video/calls/690043338 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla <> Tobias Koch | 2026-05-29 | id: 150586523 | url: https://fathom.video/calls/690043394 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-05-29 | id: 150556935 | url: https://fathom.video/calls/690043351 | recorded by Tobias Koch
- 🎯 Check-In Call | Philipp Fischer <> Tobias Koch | 2026-05-29 | id: 150545108 | url: https://fathom.video/calls/690043323 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-05-28 | id: 150293248 | url: https://fathom.video/calls/690538443 | recorded by Tobias Koch
- 🛒 Sourcing Live-Call | Tobias Koch | 2026-05-28 | id: 150227007 | url: https://fathom.video/calls/688308260 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-05-28 | id: 150203497 | url: https://fathom.video/calls/688907293 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-05-28 | id: 150196010 | url: https://fathom.video/calls/688308261 | recorded by Tobias Koch
- 🎯 Check-In Call  Call | Nicholas Hennings <> Tobias Koch | 2026-05-28 | id: 150190782 | url: https://fathom.video/calls/688308267 | recorded by Tobias Koch
- 🎯 Strategy Call Basic | Oswald Lederwaren | 2026-05-28 | id: 150152857 | url: https://fathom.video/calls/688308262 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-05-27 | id: 149868864 | url: https://fathom.video/calls/686526190 | recorded by Tobias Koch
-  🎯 Check-In | GSP Operations <> ATLAS | 2026-05-27 | id: 149834609 | url: https://fathom.video/calls/688927997 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH <> Tobias Koch | 2026-05-27 | id: 149812823 | url: https://fathom.video/calls/686526189 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-05-27 | id: 149794594 | url: https://fathom.video/calls/686526199 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-05-27 | id: 149777405 | url: https://fathom.video/calls/686526197 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Tobias Koch | 2026-05-27 | id: 149766664 | url: https://fathom.video/calls/686526195 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-05-26 | id: 149478162 | url: https://fathom.video/calls/687370022 | recorded by Tobias Koch
- 🛒 Sourcing Live-Call | Tobias Koch | 2026-05-26 | id: 149425952 | url: https://fathom.video/calls/684994713 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-05-26 | id: 149391058 | url: https://fathom.video/calls/684994716 | recorded by Tobias Koch
- 🎯 Check-In Call |  Sourcing & Einkauf: SaleLab GmbH <> ATLAS   | 2026-05-26 | id: 149351670 | url: https://fathom.video/calls/684994719 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-05-22 | id: 148782235 | url: https://fathom.video/calls/682053037 | recorded by Tobias Koch
- 🚀 Kick-Off Call |  Sourcing & Einkauf: SaleLab GmbH <> ATLAS   | 2026-05-22 | id: 148737170 | url: https://fathom.video/calls/682053036 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla <> Tobias Koch | 2026-05-21 | id: 148451548 | url: https://fathom.video/calls/673479357 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-05-21 | id: 148382075 | url: https://fathom.video/calls/682578276 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-05-21 | id: 148356176 | url: https://fathom.video/calls/682461693 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Tobias Koch | 2026-05-21 | id: 148342146 | url: https://fathom.video/calls/673479355 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-05-21 | id: 148334585 | url: https://fathom.video/calls/680403328 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Nicholas Hennings <> Tobias Koch | 2026-05-20 | id: 148016843 | url: https://fathom.video/calls/678714367 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-05-20 | id: 147941633 | url: https://fathom.video/calls/678714368 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek <> Tobias Koch | 2026-05-19 | id: 147634232 | url: https://fathom.video/calls/677252067 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-05-19 | id: 147599939 | url: https://fathom.video/calls/677252059 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-05-19 | id: 147574756 | url: https://fathom.video/calls/677252056 | recorded by Tobias Koch
- 🚤 Onboarding-Call II | Nicholas Hennings <> Tobias Koch | 2026-05-19 | id: 147563947 | url: https://fathom.video/calls/677252065 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports <> Tobias Koch | 2026-05-19 | id: 147538184 | url: https://fathom.video/calls/677252072 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-05-19 | id: 147522886 | url: https://fathom.video/calls/677252066 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen <> Tobias Koch | 2026-05-19 | id: 147508071 | url: https://fathom.video/calls/677252062 | recorded by Tobias Koch
- Followup II - offene Fragen Sourcing & Einkauf Salelab | 2026-05-18 | id: 147175755 | url: https://fathom.video/calls/674951666 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-05-18 | id: 147165162 | url: https://fathom.video/calls/674951659 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl <> Tobias Koch | 2026-05-18 | id: 147129219 | url: https://fathom.video/calls/674951661 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce <> Tobias Koch | 2026-05-18 | id: 147115313 | url: https://fathom.video/calls/674951665 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-05-15 | id: 146758566 | url: https://fathom.video/calls/673479356 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Daniel Peter <> Noah Raissi | 2026-05-15 | id: 146721387 | url: https://fathom.video/calls/674095043 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-05-14 | id: 146377719 | url: https://fathom.video/calls/671878128 | recorded by Tobias Koch
- 🎯 Re-Kick-Off | Cedric Treese <> Tobias Koch | 2026-05-13 | id: 145977171 | url: https://fathom.video/calls/670395800 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek <> Tobias Koch | 2026-05-13 | id: 145957095 | url: https://fathom.video/calls/670395801 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-05-13 | id: 145939052 | url: https://fathom.video/calls/670395803 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports <> Tobias Koch | 2026-05-13 | id: 145933630 | url: https://fathom.video/calls/670395805 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-04-15 | id: 138207380 | url: https://fathom.video/calls/636216650 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce <> Tobias Koch | 2026-04-15 | id: 138185990 | url: https://fathom.video/calls/636216648 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-04-15 | id: 138158447 | url: https://fathom.video/calls/636216645 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen <> Tobias Koch | 2026-04-15 | id: 138141957 | url: https://fathom.video/calls/636216656 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl <> Tobias Koch | 2026-04-15 | id: 138134825 | url: https://fathom.video/calls/636216646 | recorded by Tobias Koch
- 🎯 Extra Check-In Call | Saventor x ATLAS | 2026-04-15 | id: 138118270 | url: https://fathom.video/calls/636216647 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-04-15 | id: 138110874 | url: https://fathom.video/calls/636216644 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek <> Tobias Koch | 2026-04-15 | id: 138099336 | url: https://fathom.video/calls/636216651 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-04-15 | id: 138090304 | url: https://fathom.video/calls/636216649 | recorded by Tobias Koch
- 🎯 Check-In Call | Mario Bernatek <> Tobias Koch | 2026-04-14 | id: 137822692 | url: https://fathom.video/calls/634507082 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH <> Tobias Koch | 2026-04-14 | id: 137808249 | url: https://fathom.video/calls/635542785 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-04-14 | id: 137772282 | url: https://fathom.video/calls/634507117 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-04-14 | id: 137739098 | url: https://fathom.video/calls/634507085 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-04-14 | id: 137708836 | url: https://fathom.video/calls/635541722 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi <> Tobias Koch | 2026-04-10 | id: 136975707 | url: https://fathom.video/calls/630943371 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-04-10 | id: 136961420 | url: https://fathom.video/calls/633086543 | recorded by Tobias Koch
- 🎯 Check-In Call | Philipp Fischer <> Tobias Koch | 2026-04-10 | id: 136936396 | url: https://fathom.video/calls/630943369 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-04-10 | id: 136924206 | url: https://fathom.video/calls/627650205 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Tobias Koch | 2026-04-10 | id: 136917111 | url: https://fathom.video/calls/632772100 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-04-09 | id: 136632373 | url: https://fathom.video/calls/629372109 | recorded by Tobias Koch
- 🎯 Check-In Call  | Susanne Rischawy <> Tobias Koch | 2026-04-09 | id: 136606314 | url: https://fathom.video/calls/629372159 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-04-09 | id: 136597945 | url: https://fathom.video/calls/629372106 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese <> Tobias Koch | 2026-04-09 | id: 136583580 | url: https://fathom.video/calls/629372103 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-04-09 | id: 136560025 | url: https://fathom.video/calls/629372104 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek <> Tobias Koch | 2026-04-09 | id: 136535486 | url: https://fathom.video/calls/629372107 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce <> Tobias Koch | 2026-04-08 | id: 136282009 | url: https://fathom.video/calls/627650202 | recorded by Tobias Koch
- 🎯 Check-In Call | Trumost <> Tobias Koch | 2026-04-08 | id: 136248486 | url: https://fathom.video/calls/627650200 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-04-08 | id: 136235909 | url: https://fathom.video/calls/627650201 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl <> Tobias Koch | 2026-04-08 | id: 136185891 | url: https://fathom.video/calls/627650206 | recorded by Tobias Koch
-  PPC Call | Lionstrong GmbH x ATLAS - Followup II | 2026-04-08 | id: 136170907 | url: https://fathom.video/calls/627650197 | recorded by Tobias Koch
- 🎥 Call Breakdown // Sales Worksshop // Rollenspiel | 2026-04-08 | id: 136158445 | url: https://fathom.video/calls/627650198 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-04-07 | id: 135892722 | url: https://fathom.video/calls/626026566 | recorded by Tobias Koch
- 🎯 Check-In Call | Mario Bernatek <> Tobias Koch | 2026-04-07 | id: 135852887 | url: https://fathom.video/calls/622027682 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-04-07 | id: 135823438 | url: https://fathom.video/calls/626026565 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-04-07 | id: 135814213 | url: https://fathom.video/calls/626026564 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-04-07 | id: 135808825 | url: https://fathom.video/calls/626026563 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi <> Tobias Koch | 2026-04-02 | id: 134991830 | url: https://fathom.video/calls/622027677 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | HQ Sports <> Tobias Koch | 2026-04-02 | id: 134914956 | url: https://fathom.video/calls/622027676 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-04-02 | id: 134899215 | url: https://fathom.video/calls/622027679 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Design AS GmbH <> ATLAS | 2026-04-02 | id: 134882234 | url: https://fathom.video/calls/622027683 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Tobias Koch | 2026-04-02 | id: 134852527 | url: https://fathom.video/calls/623457528 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-04-02 | id: 134847247 | url: https://fathom.video/calls/622027690 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek <> Tobias Koch | 2026-04-01 | id: 134631598 | url: https://fathom.video/calls/615003176 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-04-01 | id: 134613686 | url: https://fathom.video/calls/620160661 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce <> Tobias Koch | 2026-04-01 | id: 134579227 | url: https://fathom.video/calls/620160663 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl <> Tobias Koch | 2026-04-01 | id: 134555986 | url: https://fathom.video/calls/620160656 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen <> Tobias Koch | 2026-04-01 | id: 134539702 | url: https://fathom.video/calls/620160655 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-04-01 | id: 134511983 | url: https://fathom.video/calls/620160662 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-04-01 | id: 134489712 | url: https://fathom.video/calls/620160652 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-04-01 | id: 134484836 | url: https://fathom.video/calls/620160659 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-03-31 | id: 134202508 | url: https://fathom.video/calls/618521348 | recorded by Tobias Koch
- 📈 Consulting Session | Cedric Treese <> Tobias Koch | 2026-03-31 | id: 134174888 | url: https://fathom.video/calls/618521351 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce <> Tobias Koch | 2026-03-31 | id: 134162743 | url: https://fathom.video/calls/615003166 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla <> Tobias Koch | 2026-03-31 | id: 134153592 | url: https://fathom.video/calls/618521345 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-03-31 | id: 134131017 | url: https://fathom.video/calls/618521347 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-03-30 | id: 133839663 | url: https://fathom.video/calls/617450842 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-03-30 | id: 133818464 | url: https://fathom.video/calls/616530220 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH <> Tobias Koch | 2026-03-30 | id: 133784754 | url: https://fathom.video/calls/616530219 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela <> Tobias Koch | 2026-03-27 | id: 133483227 | url: https://fathom.video/calls/615003173 | recorded by Tobias Koch
- 🎯 Check-In Call | Trumost <> Tobias Koch | 2026-03-27 | id: 133470480 | url: https://fathom.video/calls/615003170 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch <> Tobias Koch | 2026-03-27 | id: 133450771 | url: https://fathom.video/calls/615003175 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands <> Tobias Koch | 2026-03-27 | id: 133438449 | url: https://fathom.video/calls/615003165 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation <> Tobias Koch | 2026-03-27 | id: 133409385 | url: https://fathom.video/calls/615003168 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance <> Tobias Koch | 2026-03-27 | id: 133396174 | url: https://fathom.video/calls/615003180 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi <> Tobias Koch | 2026-03-27 | id: 133373366 | url: https://fathom.video/calls/615003179 | recorded by Tobias Koch
- 🎯 Check-In Call  | Susanne Rischawy <> Tobias Koch | 2026-03-27 | id: 133368052 | url: https://fathom.video/calls/615003169 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-03-27 | id: 133360246 | url: https://fathom.video/calls/615003171 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-03-27 | id: 133355102 | url: https://fathom.video/calls/615003172 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG <> Tobias Koch | 2026-03-27 | id: 133348458 | url: https://fathom.video/calls/615003178 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-03-27 | id: 133345215 | url: https://fathom.video/calls/615003177 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products <> Tobias Koch | 2026-03-27 | id: 133338508 | url: https://fathom.video/calls/615003174 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla | 2026-03-20 | id: 131592073 | url: https://fathom.video/calls/606794077 | recorded by Tobias Koch
- 🎯 Check-In Call | SK Germany X Tobias Koch | 2026-03-20 | id: 131581835 | url: https://fathom.video/calls/607158513 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek | 2026-03-20 | id: 131554982 | url: https://fathom.video/calls/606794080 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products | 2026-03-20 | id: 131543154 | url: https://fathom.video/calls/606794079 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-03-20 | id: 131521448 | url: https://fathom.video/calls/606794076 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-03-20 | id: 131516663 | url: https://fathom.video/calls/606794014 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-03-20 | id: 131509632 | url: https://fathom.video/calls/606794015 | recorded by Tobias Koch
- 🎯 Check-In Call | Mario Bernatek | 2026-03-20 | id: 131505127 | url: https://fathom.video/calls/606794013 | recorded by Tobias Koch
- 🎯 Check-In Call | Philipp Fischer | 2026-03-19 | id: 131223054 | url: https://fathom.video/calls/605291907 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-03-19 | id: 131201507 | url: https://fathom.video/calls/605291896 | recorded by Tobias Koch
- Extra Check-In Call | Pratox | 2026-03-19 | id: 131192894 | url: https://fathom.video/calls/605291903 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-03-19 | id: 131172522 | url: https://fathom.video/calls/605291904 | recorded by Tobias Koch
- 📈 Consulting Session | Cedric Treese | 2026-03-19 | id: 131159298 | url: https://fathom.video/calls/605291902 | recorded by Tobias Koch
- 🎯 Check-In Call | DIWED x ATLAS | 2026-03-18 | id: 130965209 | url: https://fathom.video/calls/603640708 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-03-18 | id: 130953402 | url: https://fathom.video/calls/603640763 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi | 2026-03-18 | id: 130933382 | url: https://fathom.video/calls/603640702 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce | 2026-03-18 | id: 130917695 | url: https://fathom.video/calls/603640764 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl | 2026-03-18 | id: 130892692 | url: https://fathom.video/calls/603640761 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen | 2026-03-18 | id: 130839393 | url: https://fathom.video/calls/603640756 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-03-18 | id: 130814450 | url: https://fathom.video/calls/603640703 | recorded by Tobias Koch
-  PPC Call | Lionstrong GmbH x ATLAS - Followup | 2026-03-18 | id: 130799397 | url: https://fathom.video/calls/603640718 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-03-18 | id: 130794700 | url: https://fathom.video/calls/603640707 | recorded by Tobias Koch
- 🎯 Check-In Call | Trumost | 2026-03-17 | id: 130554860 | url: https://fathom.video/calls/602025318 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch | 2026-03-17 | id: 130543377 | url: https://fathom.video/calls/602025322 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-03-17 | id: 130488506 | url: https://fathom.video/calls/602025319 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-03-17 | id: 130477561 | url: https://fathom.video/calls/602025314 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-03-17 | id: 130463145 | url: https://fathom.video/calls/602025313 | recorded by Tobias Koch
- 🎯 Check-In Call  | Susanne Rischawy | 2026-03-17 | id: 130456550 | url: https://fathom.video/calls/602025316 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-03-16 | id: 130064516 | url: https://fathom.video/calls/600021207 | recorded by Tobias Koch
- 🎯 Check-In Call | Orange Products | 2026-03-13 | id: 129660898 | url: https://fathom.video/calls/598462803 | recorded by Tobias Koch
- 🎯 Check-In Call | Mario Bernatek | 2026-03-13 | id: 129654209 | url: https://fathom.video/calls/598462800 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-03-13 | id: 129647427 | url: https://fathom.video/calls/598462798 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-03-12 | id: 129424226 | url: https://fathom.video/calls/596842454 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-03-12 | id: 129344948 | url: https://fathom.video/calls/596842447 | recorded by Tobias Koch
-  🎯 Check-In Call | Thomas-Christian Bärtsch | 2026-03-12 | id: 129334575 | url: https://fathom.video/calls/596842478 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-03-12 | id: 129321425 | url: https://fathom.video/calls/596842466 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla | 2026-03-12 | id: 129315908 | url: https://fathom.video/calls/596842470 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-03-12 | id: 129295756 | url: https://fathom.video/calls/596842472 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-03-12 | id: 129290299 | url: https://fathom.video/calls/596842483 | recorded by Tobias Koch
- 🎯 Check-In Call | Cedric Treese | 2026-03-12 | id: 129275434 | url: https://fathom.video/calls/596842457 | recorded by Tobias Koch
- 🎯 Check-In Call | DIWED x ATLAS | 2026-03-11 | id: 129028582 | url: https://fathom.video/calls/595136182 | recorded by Tobias Koch
-  🎯 Check-In Call | MyTropi | 2026-03-11 | id: 129005273 | url: https://fathom.video/calls/595136117 | recorded by Tobias Koch
- 🎯 Check-In Call | Trumost | 2026-03-11 | id: 128989023 | url: https://fathom.video/calls/595136180 | recorded by Tobias Koch
- 🎯 Check-In Call | GW Commerce | 2026-03-11 | id: 128969047 | url: https://fathom.video/calls/595136131 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl | 2026-03-11 | id: 128957789 | url: https://fathom.video/calls/595136130 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-03-11 | id: 128945065 | url: https://fathom.video/calls/595136140 | recorded by Tobias Koch
- 🎯 Check-In Call | SK Germany X Tobias Koch | 2026-03-11 | id: 128919274 | url: https://fathom.video/calls/595136135 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-03-11 | id: 128914358 | url: https://fathom.video/calls/595136118 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-03-11 | id: 128903257 | url: https://fathom.video/calls/595136183 | recorded by Tobias Koch
- 🎯 Check-In Call  | Susanne Rischawy | 2026-03-11 | id: 128893228 | url: https://fathom.video/calls/595136133 | recorded by Tobias Koch
- 🎯 Check-In Call | Pratox | 2026-03-11 | id: 128887219 | url: https://fathom.video/calls/595136132 | recorded by Tobias Koch
-  🎯 Check-In Call | WP Creation | 2026-03-10 | id: 128579031 | url: https://fathom.video/calls/593458664 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-03-10 | id: 128553064 | url: https://fathom.video/calls/593458665 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-03-06 | id: 127790393 | url: https://fathom.video/calls/592141404 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-03-06 | id: 127783281 | url: https://fathom.video/calls/589976792 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-03-06 | id: 127775949 | url: https://fathom.video/calls/589976638 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-03-06 | id: 127754677 | url: https://fathom.video/calls/589976863 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-03-06 | id: 127734509 | url: https://fathom.video/calls/589976696 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-03-05 | id: 127429217 | url: https://fathom.video/calls/588402998 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek | 2026-03-05 | id: 127410636 | url: https://fathom.video/calls/588402993 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-03-05 | id: 127391963 | url: https://fathom.video/calls/588403004 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-03-05 | id: 127387010 | url: https://fathom.video/calls/588403028 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-03-04 | id: 127110074 | url: https://fathom.video/calls/586774967 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla | 2026-03-04 | id: 127079811 | url: https://fathom.video/calls/586774958 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-03-04 | id: 127063839 | url: https://fathom.video/calls/586774959 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce | 2026-03-04 | id: 127051732 | url: https://fathom.video/calls/586774961 | recorded by Tobias Koch
- 🎯 Check-In Call | Pratox | 2026-03-04 | id: 127029673 | url: https://fathom.video/calls/586774966 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-03-03 | id: 126697330 | url: https://fathom.video/calls/585355672 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-03-03 | id: 126654876 | url: https://fathom.video/calls/585355677 | recorded by Tobias Koch
- 🎯 Check-In Call | Holger Schlünzen <> Luca Böse | 2026-03-03 | id: 126637225 | url: https://fathom.video/calls/585355655 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-02-27 | id: 125940324 | url: https://fathom.video/calls/581663681 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-02-26 | id: 125654448 | url: https://fathom.video/calls/579993601 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-02-26 | id: 125528985 | url: https://fathom.video/calls/579993571 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-02-26 | id: 125521108 | url: https://fathom.video/calls/579993576 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-02-25 | id: 125222012 | url: https://fathom.video/calls/578764522 | recorded by Tobias Koch
- 🎯 Check-In Call | Pratox | 2026-02-25 | id: 125155540 | url: https://fathom.video/calls/578764526 | recorded by Tobias Koch
- 🎯 Check-In Call | Christian Sobek | 2026-02-25 | id: 125143764 | url: https://fathom.video/calls/578764530 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Design AS GmbH | 2026-02-25 | id: 125135729 | url: https://fathom.video/calls/578764529 | recorded by Tobias Koch
-  PPC Audit Call | Lionstrong GmbH x ATLAS | 2026-02-24 | id: 124791030 | url: https://fathom.video/calls/576866002 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-02-20 | id: 124032252 | url: https://fathom.video/calls/573356100 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-02-20 | id: 124021435 | url: https://fathom.video/calls/573356099 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-02-20 | id: 124016326 | url: https://fathom.video/calls/573356098 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-02-20 | id: 124007789 | url: https://fathom.video/calls/573356096 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-02-20 | id: 123987104 | url: https://fathom.video/calls/573356101 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-02-20 | id: 123969718 | url: https://fathom.video/calls/573356097 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-02-19 | id: 123735345 | url: https://fathom.video/calls/571820528 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | HQ Sports | 2026-02-19 | id: 123676500 | url: https://fathom.video/calls/571820523 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2026-02-19 | id: 123653388 | url: https://fathom.video/calls/571820522 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-02-19 | id: 123640775 | url: https://fathom.video/calls/571820524 | recorded by Tobias Koch
- 🎥 Call Breakdown // Sales Worksshop // Rollenspiel | 2026-02-19 | id: 123605770 | url: https://fathom.video/calls/571820525 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla | 2026-02-18 | id: 123336866 | url: https://fathom.video/calls/570215506 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-02-18 | id: 123315622 | url: https://fathom.video/calls/570215561 | recorded by Tobias Koch
- 🎯 Check-In Call | Pratox | 2026-02-18 | id: 123251439 | url: https://fathom.video/calls/570215508 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-02-18 | id: 123239143 | url: https://fathom.video/calls/570215564 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-02-18 | id: 123233941 | url: https://fathom.video/calls/570215507 | recorded by Tobias Koch
-  📈 Consulting Call | Werkthor <> Cashflow Planung | 2026-02-17 | id: 122917348 | url: https://fathom.video/calls/570901962 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-02-13 | id: 122259839 | url: https://fathom.video/calls/565747087 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-02-13 | id: 122210336 | url: https://fathom.video/calls/565747091 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Marc Driemeyer - Pratox | 2026-02-13 | id: 122195780 | url: https://fathom.video/calls/565747086 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-02-12 | id: 121971585 | url: https://fathom.video/calls/564068790 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-02-12 | id: 121920991 | url: https://fathom.video/calls/564068615 | recorded by Tobias Koch
- 📈 Consulting Call | Saventor x ATLAS | 2026-02-12 | id: 121879693 | url: https://fathom.video/calls/564068611 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-02-12 | id: 121843884 | url: https://fathom.video/calls/564068616 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-02-12 | id: 121839436 | url: https://fathom.video/calls/564068789 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-02-11 | id: 121570612 | url: https://fathom.video/calls/562420447 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-02-11 | id: 121523675 | url: https://fathom.video/calls/562420438 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-02-11 | id: 121508372 | url: https://fathom.video/calls/562420445 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Christian Sobek | 2026-02-11 | id: 121454700 | url: https://fathom.video/calls/562420440 | recorded by Tobias Koch
- 🚤 Launch-Call | Marc Driemeyer - Pratox | 2026-02-09 | id: 120760474 | url: https://fathom.video/calls/559390227 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-02-06 | id: 120350266 | url: https://fathom.video/calls/557606429 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-02-06 | id: 120315866 | url: https://fathom.video/calls/557606441 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-02-06 | id: 120308509 | url: https://fathom.video/calls/556173541 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Marc Driemeyer - Pratox | 2026-02-06 | id: 120299593 | url: https://fathom.video/calls/557606425 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-02-05 | id: 120071081 | url: https://fathom.video/calls/556173619 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-02-05 | id: 120016946 | url: https://fathom.video/calls/556173583 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-02-05 | id: 119994348 | url: https://fathom.video/calls/556173588 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2026-02-05 | id: 119979980 | url: https://fathom.video/calls/556173580 | recorded by Tobias Koch
- 🎯 Check-In Call | Stephan Bugla | 2026-02-05 | id: 119970793 | url: https://fathom.video/calls/556173594 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-02-05 | id: 119942871 | url: https://fathom.video/calls/556173781 | recorded by Tobias Koch
- 🎥 Call Breakdown // Sales Worksshop // Rollenspiel | 2026-02-05 | id: 119925712 | url: https://fathom.video/calls/556173579 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-02-04 | id: 119632685 | url: https://fathom.video/calls/554393260 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-02-04 | id: 119620389 | url: https://fathom.video/calls/554393254 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Christian Sobek | 2026-02-04 | id: 119612251 | url: https://fathom.video/calls/554393247 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce | 2026-02-04 | id: 119605122 | url: https://fathom.video/calls/554393258 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-02-04 | id: 119574602 | url: https://fathom.video/calls/554393252 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-01-29 | id: 118206654 | url: https://fathom.video/calls/547801337 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-01-29 | id: 118143065 | url: https://fathom.video/calls/547801342 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-01-29 | id: 118128600 | url: https://fathom.video/calls/547801340 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-01-29 | id: 118119343 | url: https://fathom.video/calls/547801351 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-01-29 | id: 118111706 | url: https://fathom.video/calls/547801347 | recorded by Tobias Koch
- Florian Werner 017697558410 | 2026-01-29 | id: 118089366 | url: https://fathom.video/calls/547801339 | recorded by Tobias Koch
- Benjamin Ziehbarth | 2026-01-29 | id: 118084100 | url: https://fathom.video/calls/547801350 | recorded by Tobias Koch
- Christian Fritsch x Tobias Koch | 2026-01-29 | id: 118075814 | url: https://fathom.video/calls/547801349 | recorded by Tobias Koch
- Michael Grundwürmer 01604051732 | 2026-01-29 | id: 118067949 | url: https://fathom.video/calls/547801344 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-01-28 | id: 117813955 | url: https://fathom.video/calls/546419971 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-01-28 | id: 117797057 | url: https://fathom.video/calls/546419979 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-01-28 | id: 117774075 | url: https://fathom.video/calls/546419967 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-01-28 | id: 117757584 | url: https://fathom.video/calls/546419962 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-01-28 | id: 117743613 | url: https://fathom.video/calls/546419974 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-01-28 | id: 117715504 | url: https://fathom.video/calls/546419963 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Stephan Bugla | 2026-01-28 | id: 117702327 | url: https://fathom.video/calls/546419961 | recorded by Tobias Koch
- 🎯PPC Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2026-01-27 | id: 117370483 | url: https://fathom.video/calls/544679058 | recorded by Tobias Koch
- 🎥 Call Breakdown // Sales Worksshop // Rollenspiel | 2026-01-27 | id: 117307172 | url: https://fathom.video/calls/544678996 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-01-22 | id: 116291452 | url: https://fathom.video/calls/540024242 | recorded by Tobias Koch
- 🎯 Check-In Call | Veljet x ATLAS | 2026-01-22 | id: 116285050 | url: https://fathom.video/calls/541891062 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-01-22 | id: 116245457 | url: https://fathom.video/calls/540024240 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-01-21 | id: 115995160 | url: https://fathom.video/calls/538338303 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-01-21 | id: 115977226 | url: https://fathom.video/calls/538338301 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2026-01-21 | id: 115948001 | url: https://fathom.video/calls/538338293 | recorded by Tobias Koch
-  🎯 Check-In Cal | Lionstrong GmbH x ATLAS | 2026-01-21 | id: 115919227 | url: https://fathom.video/calls/538338302 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-01-21 | id: 115904700 | url: https://fathom.video/calls/538338297 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-01-21 | id: 115876131 | url: https://fathom.video/calls/538338299 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-01-20 | id: 115619142 | url: https://fathom.video/calls/536920696 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2026-01-20 | id: 115524091 | url: https://fathom.video/calls/536920703 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-01-20 | id: 115512970 | url: https://fathom.video/calls/536920695 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Stephan Bugla | 2026-01-19 | id: 115246537 | url: https://fathom.video/calls/535172685 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-01-16 | id: 114872660 | url: https://fathom.video/calls/533606586 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-01-16 | id: 114843596 | url: https://fathom.video/calls/533606589 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-01-16 | id: 114813121 | url: https://fathom.video/calls/533606580 | recorded by Tobias Koch
- 🎯 Check-In Call | Werkthor | 2026-01-14 | id: 114224331 | url: https://fathom.video/calls/530570363 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-01-14 | id: 114204953 | url: https://fathom.video/calls/530570353 | recorded by Tobias Koch
- 🎯 Check-In Call | Venturenaut x ATLAS  | 2026-01-14 | id: 114194325 | url: https://fathom.video/calls/530570356 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-01-14 | id: 114173071 | url: https://fathom.video/calls/530570352 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2026-01-14 | id: 114149253 | url: https://fathom.video/calls/532801314 | recorded by Tobias Koch
- Review Call | Niboline <> ATLAS | 2026-01-14 | id: 114141518 | url: https://fathom.video/calls/530570361 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Lionstrong GmbH x ATLAS | 2026-01-14 | id: 114128775 | url: https://fathom.video/calls/530570360 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2026-01-14 | id: 114113043 | url: https://fathom.video/calls/530570359 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2026-01-14 | id: 114104539 | url: https://fathom.video/calls/530570350 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | HQ Sports | 2026-01-13 | id: 113797111 | url: https://fathom.video/calls/529127522 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2026-01-13 | id: 113769035 | url: https://fathom.video/calls/529127523 | recorded by Tobias Koch
- PPC Check-In Call | BF Music | 2026-01-13 | id: 113735323 | url: https://fathom.video/calls/529127527 | recorded by Tobias Koch
- 🚀 Kick-Off mit Werkthor | 2026-01-09 | id: 112994465 | url: https://fathom.video/calls/525600820 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2026-01-08 | id: 112705083 | url: https://fathom.video/calls/524507003 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2026-01-08 | id: 112697066 | url: https://fathom.video/calls/524507002 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2026-01-07 | id: 112414133 | url: https://fathom.video/calls/523146884 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2026-01-07 | id: 112372262 | url: https://fathom.video/calls/523146873 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2026-01-07 | id: 112366999 | url: https://fathom.video/calls/523146879 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2026-01-07 | id: 112357405 | url: https://fathom.video/calls/523146893 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2026-01-05 | id: 111715814 | url: https://fathom.video/calls/520345755 | recorded by Tobias Koch
-  🎯 Extra Check-In Call |  Arthia - Sourcing | 2026-01-05 | id: 111692312 | url: https://fathom.video/calls/520345759 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-12-23 | id: 110640250 | url: https://fathom.video/calls/514917634 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-12-23 | id: 110623230 | url: https://fathom.video/calls/513425534 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-12-23 | id: 110609275 | url: https://fathom.video/calls/514263233 | recorded by Tobias Koch
- 📈 Consulting Call | Sonlib GmbH <> Sourcing | 2025-12-23 | id: 110587858 | url: https://fathom.video/calls/514263228 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-12-23 | id: 110584346 | url: https://fathom.video/calls/514263230 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-12-23 | id: 110579111 | url: https://fathom.video/calls/514263229 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-12-22 | id: 110404080 | url: https://fathom.video/calls/513169078 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Jan Eric | 2025-12-22 | id: 110375806 | url: https://fathom.video/calls/513301164 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-12-22 | id: 110346507 | url: https://fathom.video/calls/512002161 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-12-22 | id: 110334913 | url: https://fathom.video/calls/512814909 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2025-12-22 | id: 110323645 | url: https://fathom.video/calls/512814910 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-12-22 | id: 110302560 | url: https://fathom.video/calls/512814903 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-12-19 | id: 110021969 | url: https://fathom.video/calls/511465983 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-12-19 | id: 110014874 | url: https://fathom.video/calls/511465988 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-12-19 | id: 109996228 | url: https://fathom.video/calls/513114535 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2025-12-18 | id: 109729939 | url: https://fathom.video/calls/508408550 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-12-18 | id: 109692210 | url: https://fathom.video/calls/504309774 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2025-12-18 | id: 109687412 | url: https://fathom.video/calls/510124562 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-12-18 | id: 109666227 | url: https://fathom.video/calls/510124564 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-12-18 | id: 109656083 | url: https://fathom.video/calls/510124560 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-12-17 | id: 109420997 | url: https://fathom.video/calls/508408551 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2025-12-17 | id: 109360615 | url: https://fathom.video/calls/508408547 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-12-17 | id: 109310417 | url: https://fathom.video/calls/508408549 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-12-16 | id: 109045016 | url: https://fathom.video/calls/507166104 | recorded by Tobias Koch
- Sonlib x ATLAS | PPC Checkin | 2025-12-16 | id: 109021396 | url: https://fathom.video/calls/509185146 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2025-12-16 | id: 109001441 | url: https://fathom.video/calls/507166114 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-12-12 | id: 108372937 | url: https://fathom.video/calls/503861629 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce | 2025-12-12 | id: 108357481 | url: https://fathom.video/calls/503861632 | recorded by Tobias Koch
- SaleLab GmbH & Roland Vad | ATLAS Operations | Follow-Up | 2025-12-12 | id: 108332168 | url: https://fathom.video/calls/503861631 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-12-12 | id: 108326897 | url: https://fathom.video/calls/503019879 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-12-12 | id: 108290175 | url: https://fathom.video/calls/503861630 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2025-12-11 | id: 108017675 | url: https://fathom.video/calls/502352312 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | HQ Sports | 2025-12-11 | id: 107997984 | url: https://fathom.video/calls/502352310 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-12-11 | id: 107991293 | url: https://fathom.video/calls/502352314 | recorded by Tobias Koch
- 🎯 Check-In Call | Bublat GmbH & Co. KG | 2025-12-11 | id: 107957914 | url: https://fathom.video/calls/502352313 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-12-11 | id: 107949167 | url: https://fathom.video/calls/502352311 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Laurenz Elbers & Jerome Stolz | 2025-12-10 | id: 107638018 | url: https://fathom.video/calls/501301561 | recorded by Tobias Koch
- 🎯 Check-In Call | Sonlib GmbH | 2025-12-10 | id: 107616730 | url: https://fathom.video/calls/501301568 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-12-10 | id: 107611436 | url: https://fathom.video/calls/501301565 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-12-09 | id: 107309090 | url: https://fathom.video/calls/499366785 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-12-09 | id: 107275441 | url: https://fathom.video/calls/499366794 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2025-12-09 | id: 107266854 | url: https://fathom.video/calls/492996352 | recorded by Tobias Koch
- 🎯 PPC Check-In Call | Pullup & Dip x ATLAS | 2025-12-08 | id: 106960893 | url: https://fathom.video/calls/497628305 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-12-08 | id: 106913675 | url: https://fathom.video/calls/497628307 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-12-05 | id: 106630029 | url: https://fathom.video/calls/492996349 | recorded by Tobias Koch
- 🎯 PPC Check-In Call | Saventor x ATLAS | 2025-12-05 | id: 106584106 | url: https://fathom.video/calls/495979184 | recorded by Tobias Koch
- 🎯 Check-In Call | Saventor x ATLAS | 2025-12-05 | id: 106574259 | url: https://fathom.video/calls/495979183 | recorded by Tobias Koch
- 🎯 PPC Check-In Call | Iceberg | 2025-12-05 | id: 106548093 | url: https://fathom.video/calls/495979179 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce | 2025-12-04 | id: 106274853 | url: https://fathom.video/calls/494617228 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Sonlib GmbH | 2025-12-04 | id: 106250138 | url: https://fathom.video/calls/494617229 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-12-04 | id: 106235652 | url: https://fathom.video/calls/494617220 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-12-04 | id: 106231164 | url: https://fathom.video/calls/494617225 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-12-04 | id: 106208617 | url: https://fathom.video/calls/494617233 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-12-04 | id: 106196963 | url: https://fathom.video/calls/494617231 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-12-03 | id: 105922346 | url: https://fathom.video/calls/492996360 | recorded by Tobias Koch
-  📈 Consulting Call | KF Brands | 2025-12-03 | id: 105894485 | url: https://fathom.video/calls/492996354 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-12-03 | id: 105859292 | url: https://fathom.video/calls/492996365 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Saventor x ATLAS | 2025-11-28 | id: 104937306 | url: https://fathom.video/calls/488990534 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-11-28 | id: 104919467 | url: https://fathom.video/calls/488990536 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-11-28 | id: 104915049 | url: https://fathom.video/calls/490201317 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-11-28 | id: 104894997 | url: https://fathom.video/calls/488990535 | recorded by Tobias Koch
- 🎯 Check-In Call | lila-commerce | 2025-11-27 | id: 104817556 | url: https://fathom.video/calls/489130789 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Tim Fröhlich | 2025-11-27 | id: 104810211 | url: https://fathom.video/calls/487876030 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-11-27 | id: 104791345 | url: https://fathom.video/calls/484944626 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-11-27 | id: 104784223 | url: https://fathom.video/calls/487876033 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-11-27 | id: 104779374 | url: https://fathom.video/calls/487876031 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Kindaholz GmbH | 2025-11-27 | id: 104762888 | url: https://fathom.video/calls/487876029 | recorded by Tobias Koch
- Holger Hartmann <> ATLAS | 2025-11-27 | id: 104740003 | url: https://fathom.video/calls/488430076 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-11-26 | id: 104561839 | url: https://fathom.video/calls/486618255 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-11-26 | id: 104533658 | url: https://fathom.video/calls/486618253 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-11-26 | id: 104509672 | url: https://fathom.video/calls/486618248 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-11-26 | id: 104473624 | url: https://fathom.video/calls/486618242 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Mario & Benjamin Bublat | 2025-11-26 | id: 104464552 | url: https://fathom.video/calls/486618261 | recorded by Tobias Koch
- 🎥 Call Breakdown Session Bachgold // Iceberg // NTG | 2025-11-25 | id: 104141400 | url: https://fathom.video/calls/484944624 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-11-24 | id: 103774834 | url: https://fathom.video/calls/483212987 | recorded by Tobias Koch
-  📈 Consulting Call | Niboline <> ATLAS Sourcing | 2025-11-21 | id: 103440273 | url: https://fathom.video/calls/481875497 | recorded by Tobias Koch
- 🚤 Onboarding-Call | Janick Jeremy Metzger | 2025-11-21 | id: 103431476 | url: https://fathom.video/calls/481875595 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-11-21 | id: 103402036 | url: https://fathom.video/calls/481875496 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-11-21 | id: 103394473 | url: https://fathom.video/calls/481875623 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-11-20 | id: 103125211 | url: https://fathom.video/calls/480291971 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Laurenz Elbers & Jerome Stolz | 2025-11-20 | id: 103100348 | url: https://fathom.video/calls/480291966 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-11-20 | id: 103082702 | url: https://fathom.video/calls/480291968 | recorded by Tobias Koch
- 📈 Consulting Call  | Photolini <> ATLAS Sourcing | 2025-11-20 | id: 103061381 | url: https://fathom.video/calls/480291967 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-11-20 | id: 103045078 | url: https://fathom.video/calls/480291965 | recorded by Tobias Koch
- 🎯 Extra Check-In Call | BF Music <> ATLAS | 2025-11-19 | id: 102750139 | url: https://fathom.video/calls/478734728 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-11-19 | id: 102741605 | url: https://fathom.video/calls/478734722 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-11-19 | id: 102713495 | url: https://fathom.video/calls/478734732 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-11-18 | id: 102402382 | url: https://fathom.video/calls/473722913 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2025-11-17 | id: 102117649 | url: https://fathom.video/calls/475542610 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-11-17 | id: 102032382 | url: https://fathom.video/calls/475542608 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-11-14 | id: 101710674 | url: https://fathom.video/calls/473722918 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-11-14 | id: 101675289 | url: https://fathom.video/calls/473722912 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-11-14 | id: 101669531 | url: https://fathom.video/calls/475703152 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-11-14 | id: 101664964 | url: https://fathom.video/calls/473722917 | recorded by Tobias Koch
- 📈 Consulting Call  | Photolini <> ATLAS Sourcing | 2025-11-14 | id: 101655973 | url: https://fathom.video/calls/473722921 | recorded by Tobias Koch
- 🎯 Check-In Call | Feela | 2025-11-10 | id: 100359433 | url: https://fathom.video/calls/467579156 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-11-10 | id: 100345522 | url: https://fathom.video/calls/468536478 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-11-10 | id: 100334690 | url: https://fathom.video/calls/467579158 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-11-10 | id: 100294576 | url: https://fathom.video/calls/468149577 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-11-07 | id: 99998536 | url: https://fathom.video/calls/466291992 | recorded by Tobias Koch
- 🎯 Check-In Call | Photolini <> ATLAS | 2025-11-07 | id: 99989563 | url: https://fathom.video/calls/466291988 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-11-07 | id: 99943298 | url: https://fathom.video/calls/466291997 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | HQ Sports | 2025-11-06 | id: 99738568 | url: https://fathom.video/calls/464762454 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-11-06 | id: 99653929 | url: https://fathom.video/calls/464762453 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-11-06 | id: 99647806 | url: https://fathom.video/calls/464762456 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Jan Eric | 2025-11-05 | id: 99345184 | url: https://fathom.video/calls/463240921 | recorded by Tobias Koch
- Özgür <> ATLAS - Produktentwicklung // Call Breakdown | 2025-11-05 | id: 99316325 | url: https://fathom.video/calls/463240925 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-11-05 | id: 99281145 | url: https://fathom.video/calls/463240917 | recorded by Tobias Koch
- 🎯Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-11-04 | id: 98971063 | url: https://fathom.video/calls/462731296 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Vital Ventures Oldenburg GmbH <> Tobias  | 2025-11-03 | id: 98665219 | url: https://fathom.video/calls/459928448 | recorded by Tobias Koch
-  🎯 Check-In Call | Iceberg | 2025-11-03 | id: 98570564 | url: https://fathom.video/calls/459928451 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-11-03 | id: 98566478 | url: https://fathom.video/calls/460427886 | recorded by Tobias Koch
- Özgür <> ATLAS - Produktentwicklung // Call Breakdown | 2025-10-31 | id: 98306709 | url: https://fathom.video/calls/460643756 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-10-31 | id: 98285771 | url: https://fathom.video/calls/458699879 | recorded by Tobias Koch
-  🎯 Check-In Call | NTG  | 2025-10-30 | id: 98056979 | url: https://fathom.video/calls/457169680 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-10-30 | id: 97950021 | url: https://fathom.video/calls/457169679 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-10-30 | id: 97925564 | url: https://fathom.video/calls/457169675 | recorded by Tobias Koch
-  🎓 Alumni Check-In Call | Iceberg | 2025-10-30 | id: 97914088 | url: https://fathom.video/calls/454128531 | recorded by Tobias Koch
- 🎯 Check-In Call | NL Products | 2025-10-29 | id: 97655066 | url: https://fathom.video/calls/450301528 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-10-29 | id: 97626811 | url: https://fathom.video/calls/455611936 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-10-29 | id: 97605535 | url: https://fathom.video/calls/455611934 | recorded by Tobias Koch
- 🎥 Call Breakdown Session Arthia | 2025-10-29 | id: 97573940 | url: https://fathom.video/calls/455955827 | recorded by Tobias Koch
-  📈 Consulting Call | Welldora Q-Claim | 2025-10-28 | id: 97325756 | url: https://fathom.video/calls/454128537 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-10-28 | id: 97189225 | url: https://fathom.video/calls/454128541 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-10-27 | id: 96964527 | url: https://fathom.video/calls/452340969 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-10-27 | id: 96872418 | url: https://fathom.video/calls/452340968 | recorded by Tobias Koch
- 🎯 Check-In Call | Welldora | 2025-10-24 | id: 96550913 | url: https://fathom.video/calls/450993251 | recorded by Tobias Koch
- 📈 Consulting Call | Niboline <> ATLAS | 2025-10-24 | id: 96522820 | url: https://fathom.video/calls/450993253 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-10-23 | id: 96250869 | url: https://fathom.video/calls/449586624 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-10-22 | id: 95906329 | url: https://fathom.video/calls/448273992 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-10-22 | id: 95893961 | url: https://fathom.video/calls/448273985 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-10-21 | id: 95543862 | url: https://fathom.video/calls/445004132 | recorded by Tobias Koch
- 🎯 Check-In Call | Photolini <> ATLAS | 2025-10-17 | id: 94899012 | url: https://fathom.video/calls/443688678 | recorded by Tobias Koch
- Özgür <> ATLAS - Produktentwicklung // Call Breakdown | 2025-10-17 | id: 94885543 | url: https://fathom.video/calls/443688676 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call Follow up | Laurenz Elbers & Jerome Stolz | 2025-10-17 | id: 94879667 | url: https://fathom.video/calls/443688677 | recorded by Tobias Koch
- 🎯 Check-In Call | NL Products | 2025-10-16 | id: 94611596 | url: https://fathom.video/calls/442240266 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-10-16 | id: 94588199 | url: https://fathom.video/calls/442240273 | recorded by Tobias Koch
- 🎓 Alumni Check-In Call | Laurenz Elbers & Jerome Stolz | 2025-10-15 | id: 94281773 | url: https://fathom.video/calls/440750072 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports  | 2025-10-15 | id: 94258978 | url: https://fathom.video/calls/440750074 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-10-15 | id: 94253495 | url: https://fathom.video/calls/440750090 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-10-15 | id: 94234295 | url: https://fathom.video/calls/440750081 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-10-15 | id: 94220798 | url: https://fathom.video/calls/440750103 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-10-14 | id: 93957162 | url: https://fathom.video/calls/439356066 | recorded by Tobias Koch
- 🎯 Check-In Call Basic | Oswald Lederwaren | 2025-10-14 | id: 93919834 | url: https://fathom.video/calls/439356067 | recorded by Tobias Koch
-  🎯 Check-In Call |  Arthia - Sourcing | 2025-10-14 | id: 93911572 | url: https://fathom.video/calls/439356068 | recorded by Tobias Koch
- 🎯 Check-In Call | Photolini <> ATLAS | 2025-10-10 | id: 93290899 | url: https://fathom.video/calls/433857890 | recorded by Tobias Koch
-  📈 Consulting Call | Welldora Einkauf & Sourcing II | 2025-10-10 | id: 93259115 | url: https://fathom.video/calls/436814783 | recorded by Tobias Koch
-  🎯 Check-In Call | NTG  | 2025-10-09 | id: 93059339 | url: https://fathom.video/calls/435010555 | recorded by Tobias Koch
-  🎯 Check-In Call | KF Brands | 2025-10-09 | id: 92988544 | url: https://fathom.video/calls/435010548 | recorded by Tobias Koch
- 🚀 Kick-Off Call | Oswald Lederwaren <> ATLAS | 2025-10-09 | id: 92970158 | url: https://fathom.video/calls/435010551 | recorded by Tobias Koch
-  📈 Consulting Call | Welldora Einkauf & Sourcing | 2025-10-09 | id: 92949725 | url: https://fathom.video/calls/435010557 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports  | 2025-10-08 | id: 92712106 | url: https://fathom.video/calls/433857893 | recorded by Tobias Koch
- 🎯 Check-In Call | NL Products | 2025-10-08 | id: 92664274 | url: https://fathom.video/calls/433857889 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-10-08 | id: 92641317 | url: https://fathom.video/calls/433857887 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-10-08 | id: 92626874 | url: https://fathom.video/calls/433857895 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-10-08 | id: 92619094 | url: https://fathom.video/calls/433857896 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-10-07 | id: 92355267 | url: https://fathom.video/calls/432287206 | recorded by Tobias Koch
- Özgür <> ATLAS - Produktentwicklung // Call Breakdown | 2025-10-06 | id: 92007509 | url: https://fathom.video/calls/430498654 | recorded by Tobias Koch
- Extra Check-In Call | Surfin Balance | 2025-10-02 | id: 91371658 | url: https://fathom.video/calls/429688243 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports  | 2025-10-02 | id: 91353138 | url: https://fathom.video/calls/427837884 | recorded by Tobias Koch
- 📈 Consulting Call | FT Fitness - Einkauf Forecast | 2025-10-02 | id: 91333844 | url: https://fathom.video/calls/427837883 | recorded by Tobias Koch
- 🎯 Check-In Call | Photolini <> ATLAS | 2025-10-02 | id: 91328134 | url: https://fathom.video/calls/427837889 | recorded by Tobias Koch
- Özgür <> Tobias | Produktentwicklung- / Recherche Training MDD | 2025-10-01 | id: 91072718 | url: https://fathom.video/calls/423104983 | recorded by Tobias Koch
- 🎯 Check-In Call | NL Products <> Özgür Günaydin | 2025-10-01 | id: 91059109 | url: https://fathom.video/calls/426398642 | recorded by Tobias Koch
- 🎯 Check-In Call | Surfin Balance | 2025-10-01 | id: 91046970 | url: https://fathom.video/calls/426398645 | recorded by Tobias Koch
- 🎯 Check-In Call | Niboline <> ATLAS | 2025-10-01 | id: 91042715 | url: https://fathom.video/calls/426398639 | recorded by Tobias Koch
-  🎯 Check-In Call | Annabel Rahe | 2025-10-01 | id: 91024219 | url: https://fathom.video/calls/425038003 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-10-01 | id: 91014415 | url: https://fathom.video/calls/426398646 | recorded by Tobias Koch
- 🚤 Onboarding-Call Oswald Lederwaren | 2025-09-30 | id: 90747457 | url: https://fathom.video/calls/425038008 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports  | 2025-09-25 | id: 89763835 | url: https://fathom.video/calls/420567837 | recorded by Tobias Koch
- 📈 Consulting Call Sourcing & Einkauf | Surfin Balance | 2025-09-25 | id: 89738333 | url: https://fathom.video/calls/420567847 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-09-25 | id: 89703434 | url: https://fathom.video/calls/420567838 | recorded by Tobias Koch
- 🎯 Check-In Call | NL Products <> Özgür Günaydin | 2025-09-24 | id: 89433308 | url: https://fathom.video/calls/413332936 | recorded by Tobias Koch
-  🎯 Check-In Call | Annabel Rahe | 2025-09-24 | id: 89427686 | url: https://fathom.video/calls/419130782 | recorded by Tobias Koch
- 🎯 Check-In Call | Annabel Rahe <> Özgür Günaydin | 2025-09-19 | id: 88417719 | url: https://fathom.video/calls/414819382 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-09-18 | id: 88125616 | url: https://fathom.video/calls/413332930 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music | 2025-09-18 | id: 88111454 | url: https://fathom.video/calls/413332929 | recorded by Tobias Koch
-  📈 Consulting Call | HQ - CMO | 2025-09-18 | id: 88093762 | url: https://fathom.video/calls/413332937 | recorded by Tobias Koch
- 🎯 Check-In Call | Alex Kreundl <> ATLAS | 2025-09-17 | id: 87830089 | url: https://fathom.video/calls/411875500 | recorded by Tobias Koch
-  🚀 Kick-Off Call | Ocoma | 2025-09-17 | id: 87812745 | url: https://fathom.video/calls/411875496 | recorded by Tobias Koch
- 🎯 Check-In Call | BonAura <> Özgür Günaydin | 2025-09-17 | id: 87775249 | url: https://fathom.video/calls/407563544 | recorded by Tobias Koch
- Check-In | Sourcing: Tobias <> Freddy  | 2025-09-16 | id: 87499830 | url: https://fathom.video/calls/410498088 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports | 2025-09-12 | id: 86860143 | url: https://fathom.video/calls/407670829 | recorded by Tobias Koch
-  🎯 Check-In Call | Pullup & Dip | 2025-09-11 | id: 86486304 | url: https://fathom.video/calls/406215303 | recorded by Tobias Koch
- Check-In | Sourcing: Tobias <> Freddy  | 2025-09-10 | id: 86227900 | url: https://fathom.video/calls/404589030 | recorded by Tobias Koch
- 🎯 Check-In Call | BonAura <> Özgür Günaydin | 2025-09-08 | id: 85568745 | url: https://fathom.video/calls/398256104 | recorded by Tobias Koch
-  🎯 Check-In Call | Design AS | 2025-09-04 | id: 84914887 | url: https://fathom.video/calls/398931686 | recorded by Tobias Koch
- 🎯 Check-In Call | HQ Sports <> ATLAS - CRW  | 2025-09-01 | id: 84105525 | url: https://fathom.video/calls/395945768 | recorded by Tobias Koch
- 🎯 Check-In Call | Holesto  | 2025-08-28 | id: 83534060 | url: https://fathom.video/calls/392571017 | recorded by Tobias Koch
-  🎯 Check-In Call | Loumaxx GmbH | 2025-08-28 | id: 83524313 | url: https://fathom.video/calls/392571011 | recorded by Tobias Koch
- 🎯 Check-In Call | BonAura <> Özgür Günaydin | 2025-08-28 | id: 83471187 | url: https://fathom.video/calls/392571018 | recorded by Tobias Koch
-  🎯 Check-In Call |  Ecovida | 2025-08-27 | id: 83254667 | url: https://fathom.video/calls/391197048 | recorded by Tobias Koch
- 🎯 Check-In Call | Alex Kreundl <> ATLAS | 2025-08-27 | id: 83174428 | url: https://fathom.video/calls/391197033 | recorded by Tobias Koch
- 🎯 Check-In Call | Max Kneissl <> Özgür Günaydin | 2025-08-27 | id: 83169650 | url: https://fathom.video/calls/391197046 | recorded by Tobias Koch
-  🎯 Check-In Call | Design AS | 2025-08-26 | id: 82916228 | url: https://fathom.video/calls/389903985 | recorded by Tobias Koch
- 🎯 Check-In Call | BF Music <> Özgür Günaydin | 2025-08-26 | id: 82852745 | url: https://fathom.video/calls/390617470 | recorded by Tobias Koch
- 📈 Consulting Call | HQ | 2025-08-20 | id: 81724028 | url: https://fathom.video/calls/385308000 | recorded by Tobias Koch
- Test 3 | 2025-08-20 | id: 81682688 | url: https://fathom.video/calls/386339991 | recorded by Tobias Koch
- Test X | 2025-08-20 | id: 81681922 | url: https://fathom.video/calls/386326721 | recorded by Tobias Koch
- Test final | 2025-08-18 | id: 81089006 | url: https://fathom.video/calls/383868148 | recorded by Tobias Koch
- Test12 | 2025-08-18 | id: 81083841 | url: https://fathom.video/calls/383826402 | recorded by Tobias Koch
- Test 9 | 2025-08-18 | id: 81082906 | url: https://fathom.video/calls/383811213 | recorded by Tobias Koch
"""

# Meetings where Tobias participated but recorded by colleagues (from find_person)
# Format: (date, title, recorded_by, id, url)
OTHERS = [
    ("2026-05-29", "🚀 Daily Huddle", "Konstantin Müllner", "150522973", "https://fathom.video/calls/690601706"),
    ("2026-05-20", "Tobias Koch", "Konstantin Müllner", "148059017", "https://fathom.video/calls/681351403"),
    ("2026-05-20", "Tobias Koch", "Konstantin Müllner", "148089964", "https://fathom.video/calls/681409746"),
    ("2026-05-19", "Daily Huddle 🚀", "Konstantin Müllner", "147497104", "https://fathom.video/calls/677310226"),
    ("2026-05-15", "Tobias Koch", "Konstantin Müllner", "146804227", "https://fathom.video/calls/675808852"),
    ("2025-10-13", "🎯 Check-In Call | NTG", "Mario Schäfer", "93643499", "https://fathom.video/calls/437853512"),
    ("2025-09-30", "🎯 Check-In Call | Loumaxx GmbH", "Mario Schäfer", "90779124", "https://fathom.video/calls/425117652"),
    ("2025-09-29", "🎯 Check-In Call | KF Brands <> Tobias Koch", "Özgür Günaydin", "90415791", "https://fathom.video/calls/423527108"),
    ("2025-09-26", "🎯 Check-In Call | Photolini <> ATLAS", "Özgür Günaydin", "90093162", "https://fathom.video/calls/423987910"),
    ("2025-09-26", "📈 Consulting Call | BF - Sourcing & Einkauf", "Özgür Günaydin", "90027485", "https://fathom.video/calls/422109058"),
    ("2025-09-25", "Zoom Meeting von Özgür Günaydin (Vorstellung Tobias - Team Iceberg)", "Özgür Günaydin", "89720699", "https://fathom.video/calls/422301660"),
    ("2025-09-25", "Laurenz Elbers & Jerome Stolz: 🎓 Alumni Check-In Call", "Özgür Günaydin", "89751881", "https://fathom.video/calls/422462795"),
    ("2025-09-11", "Consulting: BF Music x Atlas", "Alexander Schefstoss", "86520001", "https://fathom.video/calls/406413883"),
    ("2025-09-10", "🎯 Check-In Call | Alex Kreundl <> ATLAS", "Özgür Günaydin", "86255745", "https://fathom.video/calls/404589010"),
    ("2025-09-10", "🎯 Check-In Call | BF Music", "Özgür Günaydin", "86166269", "https://fathom.video/calls/404588993"),
    ("2025-09-05", "🎯 Check-In Call | Gebrüder Wehle", "Mario Schäfer", "85212572", "https://fathom.video/calls/400245568"),
    ("2025-09-04", "🎯 Check-In Call | Animalea", "Mario Schäfer", "84992084", "https://fathom.video/calls/399058469"),
    ("2025-09-04", "Call Breakdown (Vorstellung Tobias / Roadmap)", "Özgür Günaydin", "84920719", "https://fathom.video/calls/399058236"),
    ("2025-09-03", "🎯 Check-In Call | Alex Kreundl <> ATLAS", "Özgür Günaydin", "84546965", "https://fathom.video/calls/397285104"),
    ("2025-09-02", "🚀 Kick Off | Venturenaut x ATLAS Operations", "Mario Schäfer", "84229311", "https://fathom.video/calls/396432674"),
    ("2025-08-29", "Tobias | Produktentwicklung- / Recherche Training MDD", "Özgür Günaydin", "83784116", "https://fathom.video/calls/393977867"),
    ("2025-08-28", "🎯 Check-In Call | Gebrüder Wehle", "Mario Schäfer", "83503713", "https://fathom.video/calls/392426180"),
    ("2025-08-28", "🎯 Check-In Call | NL Products", "Özgür Günaydin", "83477658", "https://fathom.video/calls/389906475"),
    ("2025-08-27", "🎯 Check-In Call | Florian & Andreas <> ATLAS", "Özgür Günaydin", "83237527", "https://fathom.video/calls/391313976"),
    ("2025-08-26", "🎯 Check-In Call | 7matters", "Özgür Günaydin", "82903507", "https://fathom.video/calls/389906480"),
    ("2025-08-25", "Zoom Meeting von Özgür Günaydin (Sourcing-Fortschritt)", "Özgür Günaydin", "82594058", "https://fathom.video/calls/390438495"),
    ("2025-08-22", "🎯 Check-In Call | Animalea", "Mario Schäfer", "82295288", "https://fathom.video/calls/387308606"),
    ("2025-08-22", "🎯 Check-In Call | Brand Promotion", "Mario Schäfer", "82292137", "https://fathom.video/calls/384544020"),
    ("2025-08-22", "📈 Consulting Call | Loumaxx GmbH", "Mario Schäfer", "82272939", "https://fathom.video/calls/387308532"),
    ("2025-08-20", "📈 Consulting Call | NTG", "Mario Schäfer", "81692880", "https://fathom.video/calls/384544019"),
    ("2025-08-20", "🎯 Check-In Call | Design AS", "Mario Schäfer", "81686630", "https://fathom.video/calls/384544018"),
    ("2025-08-20", "🎯 Check-In Call | Daniel Göser", "Mario Schäfer", "81669040", "https://fathom.video/calls/384544021"),
    ("2025-08-19", "🎯 Check-In Call | Lars Schultka", "Mario Schäfer", "81438196", "https://fathom.video/calls/383440862"),
    ("2025-08-19", "🎯 Check-In Call | Gebrüder Wehle", "Mario Schäfer", "81416948", "https://fathom.video/calls/383440859"),
    ("2025-08-14", "🚀 Kick-Off Call | Daniel Göser", "Mario Schäfer", "80506575", "https://fathom.video/calls/379612546"),
]

pattern = re.compile(r'^\s*-\s*(.+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*id:\s*(\d+)\s*\|\s*url:\s*(\S+)\s*\|\s*recorded by\s+(.+?)\s*$')

rows = {}  # id -> (date, title, recorded_by, url)
for line in RAW.splitlines():
    if not line.strip():
        continue
    m = pattern.match(line)
    if not m:
        # try without "recorded by" suffix robustness
        continue
    title, date, rid, url, rec = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    title = re.sub(r'\s+', ' ', title).strip()
    rows[rid] = (date, title, rec.strip(), url)

for date, title, rec, rid, url in OTHERS:
    if rid not in rows:
        rows[rid] = (date, title, rec, url)

# sort by date desc, then id desc
items = sorted(rows.values(), key=lambda r: (r[0], r[3]), reverse=True)

with open("tobias_koch_fathom_alle_calls.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Nr", "Datum", "Titel", "Aufgezeichnet von", "Link"])
    for i, (date, title, rec, url) in enumerate(items, 1):
        w.writerow([i, date, title, rec, url])

print(f"Total unique meetings: {len(items)}")
# quick type breakdown
from collections import Counter
def kind(t):
    tl = t.lower()
    if "sourcing live" in tl: return "Sourcing Live-Call"
    if "office-hour" in tl: return "Daily Office-Hour"
    if "kick-off" in tl or "kick off" in tl: return "Kick-Off"
    if "onboarding" in tl: return "Onboarding"
    if "consulting" in tl: return "Consulting"
    if "ppc" in tl: return "PPC"
    if "call breakdown" in tl: return "Call Breakdown"
    if "strategy" in tl: return "Strategy"
    if "alumni" in tl: return "Alumni Check-In"
    if "check-in" in tl or "check in" in tl: return "Check-In"
    if "daily huddle" in tl: return "Daily Huddle"
    return "Sonstige"
c = Counter(kind(t) for (_, t, _, _) in items)
for k, v in c.most_common():
    print(f"  {k}: {v}")
