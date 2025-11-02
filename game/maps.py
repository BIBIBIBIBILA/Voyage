# === File Overview (auto-generated) ===
# Project: USYD Tower Adventure
# File: usyd_adventure_pygame_update2_run/game/maps.py
# Purpose: Map/tile handling: loading maps, collisions, coordinates, and rendering layers.
#
# Key Notes:
# - Map/tile handling: loading maps, collisions, coordinates, and rendering layers.
# - Key/Inventory handling present.
# - Door mechanics present.
#
# Run instructions:
# - Recommended entry script: main.py (or any file with __main__ guard).
# - Example: `python main.py` from the project root.
#
# This header was auto-generated to help readers navigate the codebase.

plane = [
"(sky)(sky)(sky)(sky)(sky)(wingsRE)(sky)(sky)(sky)(sky)(sky)(sky)(sky)",
 "(sky)(sky)(sky)(sky)(sky)(wingLB)(wingR)(sky)(clo)(sky)(sky)(sky)(sky)",
"#(sky)(sky)(clo)(sky)(wingLB)(wings)(sky)(sky)(clo)(sky)(sky)(sky)",
 "#X(sky)(sky)(sky)(wingLB)(wings)(sky)(sky)(sky)(sky)(sky)(sky)",
"#XXXXXXXXXXX(sky)",
 "#XX.X.X.X.X.#",
"#(os)....(ps)....(au)#",
"#XXXXXXXXXXX(sky)",
 "(sky)(sky)(sky)(sky)(sky)(wingLB)(wings)(sky)(sky)(sky)(sky)(sky)(clo)",
"(sky)(sky)(sky)(sky)(sky)(wingLB)(wings)(sky)(sky)(sky)(sky)(sky)(sky)",
"(sky)(sky)(clo)(sky)(sky)(wingLB)(wings)(sky)(clo)(sky)(sky)(sky)(sky)",
"(sky)(sky)(sky)(sky)(clo)(wingLB)(wingsL)(sky)(sky)(sky)(sky)(clo)(sky)",
 "(sky)(sky)(sky)(sky)(sky)(wingsE)(sky)(sky)(sky)(clo)(sky)(sky)(sky)",
]

customs = [
"#############",
"#(ua)###########",        #ua:customs to plane
"#.###########",
"#.....#.....#",
"####(p0)(k14)#.#.#.#",        #p0:person check server. k14:key14 to door14(after customer clean could get the key14)
"#.(d14)...#.....#",            #d14:door14 need k14
"#.#####.#.#.#",
"#...........#",
"#####(d0)#####.#",        #d0:door1 need k1
"#...#.....#.#",
"#...#.#.#.#.#",
"#...#..(tk)..#(up)#",        #tk:ticket. up:customs to airport
"#############",
]

airport = [
"#############",
"#(pu)#.......###",        #pu:airport to customs
"#.####(p1)######",        #p1:person1,server
"#.#.......###",
"#.###...#####",
"#...........#",
"#...........#",
"#...........#",
"#...........#",
"##.........##",
"###.......###",
"####..(ac)..####",        #ac:airport to campus
"#############",
]

# Campus: doors guarding letter gates
campus = [
"#############",
"#(cl)..#.(ca).##.(cq)#",        #cl:campus to library. ca：campus to airport.cq：campus to quadrangle
"#...#...##..#",
"###.#...##..#",
"###.#...(d1)...#",        #d1:door1 need k1
"###(d2)#...#####",        #d2：door2 need k2
"#(cd).........(cs)#",     #cd：campus to dorm. cs：campus to center
"###(d3)#.......#",        #d3：door3 need k3
"###.#...#.#.#",
"#...#....#(b4).#",        #b4: book4
"#...#...#.#.#",
"#(ce)..#.(cm).....#",        #ce：campus to engineering cm：campus to market
"#############",
]

# Student Center: inner G door (needs lounge_key + green key)
student_center = [
"#############",
"##...#(p2)#...##",        #p2：person2 student
"#(p3).........(p4)#",        #p3/p4：person3/4 student
"##.........##",
"#...##.##...#",
"######(d4)######",        #d4：door4 need k4
"#(sc)..........#",        #sc：center to campus
"######..###(d5)#",        #d5:door5 need k5
"#...##..###.#",
"#.(k9).....#..(k3)#",        #k9:get idcard key9 to door9 k3：key3 to door3
"#...##..#(d6)###",        #d6:door6 need k6
"######..#..(se)#",        #se：S1 sheet
"#############",
]

# Dorm: item lines behind simple layout
dorm = [
"#############",
"#.(k5)..#.#...(k4)#",        #k5: k5 to door5. k4:key4 to door4
"#.(p5)..(d7).(d8)..(p6).#",        #d7/d8：door7/door8 need k7/k8. p5/p6：person student
"#....#.#....#",
"#....#.#....#",
"######.######",
"#(dr).........(dc)#",        #dr：dorm to rooftop. dc:dorm to campus
"#......######",
"#.#(p7)#..#....#",        #p7：person student
"#......#..(re1).#",        #re1: rest point
"#.#(p8)#..(d9)....#",        #d9：door9 need k9
"#......#..(bc)(k1)#",        #bc: bus card unlock market. k1:key1 to door1
"#############",
]

rooftop = [
"(sky)(sky)###########",
"(sky)(sky)###########",
"(sky)(sky)#..(k7)..#####",        #k7:key7 to door7
"(clo)(sky)#.....#####",
"(sky)(sky)#.....#####",
"(sky)(sky)#.....#####",
"(sky)(sky)#.(re2)...(d10)..(rd)#",        #re2: rest point. d10:door10 need k10. rd:rooftop to dorm
"(sky)(sky)#.....#####",
"(sky)(clo)#.....#####",
"(sky)(sky)#.....#####",
"(clo)(sky)#.....#####",
"(sky)(sky)###########",
"(sky)(sky)###########",
]

# Library: two items (eng key; lounge_key + green key)
library = [
"#############",
"#.......#...#",
"#.##(b3)##.(d11).(ne).#",        #d11：door11 need k11. ne：smart note
"#.......#...#",
"#.##....#####",
"#.(p9)#........#",        #p9：person library server chat with to get k12(Canvas app)
"#.##....#...#",
"#.......#...#",
"#.#(b1)###.#...#",        #b1:book1
"#.......#...#",
"#.###(b2)#.#...#",        #b2:book2
"#.......#..(lc)#",        #lc:library to campus
"#############",
]

engineering = [
"#############",
"#(ec)#..###....#",        #ec:engineering to campus
"#.#.##......#",
"#.##...#....#",
"#.#...#...###",
"#.#..#....#.#",
"#.(d12).......(p10).#",        #d12:door12 need k12. p10:person lecturer
"#.#..#....#.#",
"#.#...(le)...###",        #le:listen to lecture
"#.##...#....#",
"#.#.##......#",
"#(el)#..###....#",        #el:engineering to lab
"#############",
]


lab = [
"#############",
"#(le)###########",         #le:lab to engineering
"#.###########",
"#.###########",
"#.#.........#",
"#.#.##...##.#",
"#......(p11)....#",        #p11:person tutor
"#.#.##...##.#",
"#.#(k2)........#",         #k2:key2 to door2
"#############",
"#############",
"#############",
"#############",
]

quadrangle = [
"(sky)(sky)(sky)(sky)(sky)(sky)#(sky)(sky)(sky)(sky)(sky)(sky)",
"(sky)(sky)(sky)(sky)(sky)#(al)#(sky)(sky)(sky)(sky)(sky)",
"(sky)(sky)(clo)(sky)(sky)#(mw)#(sky)(sky)(sky)(sky)(sky)",
"(sky)(sky)(sky)(sky)#...#(sky)(sky)(clo)(sky)",
"(sky)(sky)(sky)(sky)#...#(sky)(sky)(sky)(sky)",
"(sky)(sky)(clo)#(k10)....#(sky)(sky)(sky)",
"(sky)(sky)(sky)#.....#(sky)(clo)(sky)",
"(sky)(sky)#.......#(sky)(sky)",
"(clo)(sky)#.......#(sky)(sky)",
"(sky)#.........#(sky)",
"(sky)#.........#(clo)",
"#.....(qc).....#",
"#############",
]

market = [
"#############",
"#.#.#.(mc).#...#",        #mc:market to campus
"#...#...#...#",
"#.#.#...#...#",
"#...#...#...#",
"#.#.#...#####",
"#...(p12)......(mh)#",        #p12:person market server, chat with to exchange harbour photo to k8(key8 to door8). mh:market to harbour
"#.#.####.####",
"#...#....#..#",
"#.#.#....(p13)..#",        #p13:person coffee server, chat with to exchange coffee photo to k13(key13 to door13)
"#...#..(cf).####",        #cf:drink coffee
"#.#.#......(cp)#",        #cp:coffee bar photo
"#############",
]

harbour = [
"(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)",       #hm:harbour to market
"(sea)(sea)(sea)#(sea)(sea)(sea)#(sea)(sea)(sea)(sea)(sea)",
"(sea)#(sea)(sea)###(hm)#(sea)(sea)(sea)(sea)",
"(sea)(sea)#(sea)#.#.##(sea)(sea)(sea)",
"(sea)(sea)##...(d13)..#(sea)(sea)",
"(sea)#..#.(hp).#..#(sea)",
"#############",
"#############",
"(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)",
"(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)",        #d13：door13 need k13
"(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)",        #hp:harbour photo
"(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)(sea1)",
"(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)(sea)",
]



street_campus_to_market = [
"(grass1)(grass1)(grass1)(grass1)(grass1)#(tc)#(grass1)(grass1)(grass2)(grass1)(grass1)",
"(grass1)(grass1)(grass2)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass3)(grass1)(grass2)(grass1)(grass2)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass2)(grass1)(grass3)(grass1)(grass2)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass2)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass2)(grass1)",
"(grass1)(grass1)(grass1)(grass2)(grass1)#.#(grass1)(grass2)(grass1)(grass1)(grass1)",
"(grass2)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass2)(grass1)(grass1)(grass2)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass1)(grass2)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass2)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass3)(grass1)(grass2)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#(tm)#(grass1)(grass1)(grass2)(grass1)(grass1)",
]

street_airport_to_campus = [
"(grass1)(grass1)(grass1)(grass1)(grass1)#(at)#(grass1)(grass1)(grass2)(grass1)(grass1)",
"(grass1)(grass1)(grass2)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass3)(grass1)(grass1)(grass1)(grass2)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass2)(grass1)(grass3)(grass1)(grass1)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass2)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass2)(grass1)",
"(grass1)(grass1)(grass3)(grass2)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass2)(grass1)(grass1)(grass2)",
"(grass1)(grass2)(grass1)(grass1)(grass1)#.#(grass1)(grass2)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass2)(grass1)(grass1)(grass1)(grass1)#.#(grass1)(grass1)(grass1)(grass3)(grass1)",
"(grass1)(grass3)(grass1)(grass2)(grass1)#.#(grass1)(grass1)(grass1)(grass1)(grass1)",
"(grass1)(grass1)(grass1)(grass1)(grass1)#(tu)#(grass1)(grass1)(grass2)(grass1)(grass1)",
]

levels = {
    "plane": plane,
    "customs": customs,
    "airport": airport,
    "campus": campus,
    "student_center": student_center,
    "dorm": dorm,
    "rooftop": rooftop,
    "library": library,
    "engineering": engineering,
    "lab": lab,
    "quadrangle": quadrangle,
    "market": market,
    "harbour": harbour,
    "street_campus_to_market": street_campus_to_market,
    "street_airport_to_campus": street_airport_to_campus
}