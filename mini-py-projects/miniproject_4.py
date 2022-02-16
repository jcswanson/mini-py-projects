# MiniProject 4 : A Quality Control business!
# John Swanson CMPSCI 101
# Feb 15, 2022
print("<<<---------------------------    QUALITY CONTROL MEASUREMENT SOFTWARE FOR TOLERANCING    ---------------------------------->>>")
print("Record measurements of parts made for a machine and if each part measurement is within the +/- 1 inch tolerance")
print("you, the inspector, can proceed inspecting parts for the business. But beware the machine has a tolerance too.")
print("At the end if the assembled parts inches out of tolerance summed is < 2.5 inches then the parts are assembled together and can ship!")

total_out_of_tolerance = 0
part_count = 0

dimension_1 = float(input("Dimension 1 (5.00in): "))
print(dimension_1)
if abs(dimension_1 - 5) > 1.0:
    print(str("Send part back for machining, must be +/- 1.0 inches of blueprint design. %.2f"%(dimension_1-5) + " inches out of tolerance!"))
else:
    part_count += 1
    total_out_of_tolerance += abs(dimension_1 - 5)

dimension_2 = float(input("Dimension 2 (9.00in): "))
print(dimension_2)
if abs(dimension_2 - 9) > 1.0:
    print(str("Send part back for machining, must be +/- 1.0 inches of blueprint design. %.2f"%(dimension_2-9) + " inches out of tolerance!"))
else:
    part_count += 1
    total_out_of_tolerance += abs(dimension_2 - 9)

dimension_3 = float(input("Dimension 3 (12.00in): "))
print(dimension_3)
if abs(dimension_3 - 12) > 1.0:
    print(str("Send part back for machining, must be +/- 1.0 inches of blueprint design. %.2f"%(dimension_3-12) + " inches out of tolerance!"))
else:
    part_count += 1
    total_out_of_tolerance += abs(dimension_3 - 12)

if  part_count == 3:
    if total_out_of_tolerance <= 2.5:
        print(str("CONGRATULATIONS your machine shipped with all 3 parts! It was out of tolerance by only %.2f"%total_out_of_tolerance + " inches"))
    if total_out_of_tolerance > 2.5:
        print(str("Sorry the customer rejected your machine as it was too out of tolerance by %.2f"%total_out_of_tolerance + " inches"))
else:
    print("Good job you have " + str(part_count) + " out of 3 parts needed to finish machine. Remachine the missing parts and try again!")   