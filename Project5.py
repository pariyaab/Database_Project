import sqlite3
from sqlite3 import Error
import secrets
from datetime import date
from datetime import datetime

from prettytable import PrettyTable


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("pragma foreign_keys = on")
    except Error as e:
        print(e)
    return conn


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


######### INSERT OPERATION #########

def insert_to_user(conn):
    cursor = conn.cursor()
    try:
        first_name = input("Enter first_name >> ")
        last_name = input("Enter last_name >> ")
        phone_number = input("Enter phone number >> ")
        token = secrets.token_hex(50)
        role = int(input("Is the user a normal or an admin? 1 for admin and 2 for normal user >> "))
        user_name = input("Enter user name and must be unique >> ")
        age = int(input("Enter age >> "))
        password = input("Enter password >> ")
        national_number = input("Enter national number and must be unique >> ")
        picture = input("Enter a path for user picture (Optional) and if yo do'nt add pic enter -1 >> ")
        if picture != '-1':
            photo = convertToBinaryData(picture)
            cursor.execute("""
            INSERT INTO User(first_name,last_name,phone_number, token,role,picture,user_name,age,password,national_number)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (first_name, last_name, phone_number, token, role, photo, user_name, age, password, national_number))
            conn.commit()
            print("user successfully added ")
            return True
        else:
            cursor.execute("""
            INSERT INTO User(first_name,last_name,phone_number, token,role,user_name,age,password,national_number)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (first_name, last_name, phone_number, token, role, user_name, age, password, national_number))
            conn.commit()
            print("user successfully added ")
            return True

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into user table", error)


def insert_to_vehicles(conn):
    cursor = conn.cursor()
    try:
        name = input("Enter model vehicle >> ")
        color = input("Enter color vehicle >> ")
        engine_volume = float(input("Enter engine volume >> "))
        copmany = input("Enter the vehicle manufacturer >> ")
        country = input("Enter the country of manufacture of the vehicle >> ")
        engine_power = float(input("Enter engine power >> "))
        plaque = input("Enter plaque >> ")
        function = input("Enter function >> ")
        is_painted = input("Is your vehicle painted? Y/N >> ")
        if is_painted == 'Y':
            is_painted = True
        else:
            is_painted = False
        state_city = input("Enter the city of the sale >> ")
        state_the_neighbourhood = input("Enter the neighbourhood of the sale >> ")
        year_construction = int(input("Enter the construction year >> "))
        is_installment = input("Is your vehicle for sale in installments? Y/N ")
        if is_installment == 'Y':
            is_installment = True
        else:
            is_installment = False
        accelleration = float(input("Enter the accelleration >> "))
        gearbox = input("Enter the type of vehicle gearbox? Gear or automatic >> ")
        fuel_type = input("Enter the fuel type of the vehicle? Gasoline or gas >> ")
        veh_picture = input("Enter a path for vehicle picture (Optional) and if yo do'nt add pic enter -1 >> ")
        user_name = input("Enter user_name Seller >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        price = int(input("Enter the price >> "))
        type = int(input("Enter your vehicle type. 0 for cars and 1 for motorcycles >> "))
        level = 'economic'
        if accelleration > 20 and engine_power > 1200:
            level = 'economic'
        elif accelleration > 40 and engine_power > 1400:
            level = 'luxury'
        elif accelleration > 50 and engine_power > 1500:
            level = 'sport'
        if veh_picture == '-1':
            cursor.execute("""
            INSERT INTO VehicleInformation(name ,color,engine_volume, copmany ,country ,engine_power,plaque ,function ,is_painted ,level ,
            state_city,state_the_neighbourhood,
            year_construction,is_installment,accelleration,gearbox,fuel_type,user_id,price,type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                name, color, engine_volume, copmany, country, engine_power, plaque, function, is_painted, level,
                state_city,
                state_the_neighbourhood,
                year_construction, is_installment, accelleration, gearbox, fuel_type, user_id, price, type))
            conn.commit()
            cursor.close()
            print("Vehicle inserted successfully !")
            return True

        if veh_picture != '-1':
            photo = convertToBinaryData(veh_picture)
            cursor.execute("""
            INSERT INTO VehicleInformation(name ,color,engine_volume, copmany ,country ,engine_power,plaque ,function ,is_painted ,level ,
            state_city,state_the_neighbourhood,
            year_construction,is_installment,accelleration,gearbox,fuel_type,veh_picture,user_id,price,type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                name, color, engine_volume, copmany, country, engine_power, plaque, function, is_painted, level,
                state_city,
                state_the_neighbourhood,
                year_construction, is_installment, accelleration, gearbox, fuel_type, photo,
                user_id, price, type))
            conn.commit()
            cursor.close()
            print("Value inserted successfully with picture!")
            return True
    except sqlite3.Error as error:
        print("Failed to insert data into vehicle table", error)


def insert_to_post(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter post sharing user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        date1 = input("Enter the posting date and enter 1 to use the current date >> ")
        if date1 == '1':
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            date1 = d1
            print("date =", date1)
        time = input("Enter the posting time and enter 1 to use the current time >> ")
        if time == '1':
            time = datetime.today().strftime("%H:%M %p")
        cursor.execute("""
                INSERT INTO Post(user_id,date,time)
                VALUES (?,?,?)
                """,
                       (user_id, date1, time))
        conn.commit()
        cursor.close()
        print("post successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into post table", error)


def insert_to_post_vehicles(conn):
    cursor = conn.cursor()
    try:
        post_id = int(input("Enter the post id >> "))
        vehicle_id = int(input("Enter the post sharing vehicle id >> "))
        cursor.execute("""
                        INSERT INTO PostVehicles(post_id,vehicle_id)
                        VALUES (?,?)
                        """,
                       (post_id, vehicle_id))
        conn.commit()
        cursor.close()
        print("post successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Post Vehicles table", error)


def insert_to_favorite_vehicles(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        plaque = input("Enter the plaque of the vehicle for which you like the post >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        cursor.execute("""
                           INSERT INTO FavoriteVehicles(user_id,post_id)
                           VALUES (?,?)
                           """,
                       (user_id, post_id))
        conn.commit()
        cursor.close()
        print("Favorite Vehicles successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Favorite Vehicles table", error)


def insert_to_archive_vehicles(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        plaque = input("Enter the plaque of the vehicle for which you archive the post >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        cursor.execute("""
                           INSERT INTO ArchiveVehicles(user_id,post_id)
                           VALUES (?,?)
                           """,
                       (user_id, post_id))
        conn.commit()
        cursor.close()
        print("Archive Vehicles successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Archive Vehicles table", error)


def insert_to_fail_vehicles(conn):
    cursor = conn.cursor()
    try:
        description = input("Enter description >> ")
        user_name = input("Enter user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        plaque = input("Enter the plaque of the vehicle for which you fail the post >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        cursor.execute("""
                           INSERT INTO FailVehicles(description,user_id,post_id)
                           VALUES (?,?,?)
                           """,
                       (description, user_id, post_id))
        conn.commit()
        cursor.close()
        print("Fail Vehicles successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Fail Vehicles table", error)


def insert_to_put_comment(conn):
    cursor = conn.cursor()
    try:
        date1 = input("Enter the posting date and enter 1 to use the current date >> ")
        if date1 == '1':
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            date1 = d1
            print("date =", date1)
        time = input("Enter the posting time and enter 1 to use the current time >> ")
        if time == '1':
            time = datetime.today().strftime("%H:%M %p")
        text = input("Enter your comment text >> ")
        user_name = input("Enter user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        plaque = input("Enter the plaque of the vehicle for which you want to comment on it >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        cursor.execute("""
                        INSERT INTO PutComment(time,date,text,user_id,post_id)
                        VALUES (?,?,?,?,?)
                        """,
                       (time, date1, text, user_id, post_id))
        conn.commit()
        cursor.close()
        print("comment successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into comment table", error)


def insert_section(conn):
    cursor = conn.cursor()
    try:
        name = input("Enter section name >> ")
        cursor.execute("""
                           INSERT INTO Section(name)
                           VALUES (?)
                           """, (name,))
        conn.commit()
        cursor.close()
        print("section successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into section table", error)


def insert_permission(conn):
    cursor = conn.cursor()
    try:
        name = input("Enter permission name >> ")
        cursor.execute("""INSERT INTO Permission(name) VALUES (?)
                           """, (name,))
        conn.commit()
        cursor.close()
        print("Permission successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Permission table", error)


def insert_user_permission(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter user name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user id is :", user_id)
        name_permission = input("Enter name permission >> ")
        permission_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("permission id : ", permission_id)
        cursor.execute("""
                           INSERT INTO UserPermission(user_id,permission_id)
                           VALUES (?,?)
                           """,
                       (user_id, permission_id,))
        conn.commit()
        cursor.close()
        print("User Permission successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into User Permission table", error)


def insert_section_permission(conn):
    cursor = conn.cursor()
    try:
        section_id = int(input("Enter section id >> "))
        permission_id = int(input("Enter Permission id >> "))
        cursor.execute("""INSERT INTO SectionPermission(section_id,permission_id) VALUES (?,?)""",
                       (section_id, permission_id))
        conn.commit()
        cursor.close()
        print("Section Permission successfully added ")
        return True
    except sqlite3.Error as error:
        print("Failed to insert data into Section Permission table", error)


def inset_to_tables(conn):
    print_tables_name()
    table_choice = int(input("Which table are you going to add ? "))
    if table_choice == 1:
        return insert_to_user(conn)
    elif table_choice == 2:
        return insert_to_vehicles(conn)
    elif table_choice == 3:
        return insert_to_post(conn)
    elif table_choice == 4:
        return insert_to_post_vehicles(conn)
    elif table_choice == 5:
        return insert_to_favorite_vehicles(conn)
    elif table_choice == 6:
        return insert_to_archive_vehicles(conn)
    elif table_choice == 7:
        return insert_to_fail_vehicles(conn)
    elif table_choice == 8:
        return insert_to_put_comment(conn)
    elif table_choice == 9:
        return insert_section(conn)
    elif table_choice == 10:
        return insert_permission(conn)
    elif table_choice == 11:
        return insert_user_permission(conn)
    else:
        return insert_section_permission(conn)


######### MENU AND TABLE NAMES #########

def print_tables_name():
    print("1.  User Table")
    print("2.  Vehicles Information Table")
    print("3.  Post Table")
    print("4.  Post Vehicles Table")
    print("5.  Favorite Vehicles Table")
    print("6.  Archive Vehicles Table")
    print("7.  Fail Vehicles Table")
    print("8.  PutComment Table")
    print("9.  Section Table")
    print("10. Permission Table")
    print("11. User Permission Table")
    print("12. Section Permission Table")


def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Insert To Tables")
    print("2. Fetch Tables")
    print("3. Delete Tables")
    print("4. Update Tables")
    print("5. Special Queries")
    print("6. Exit")
    print(67 * "-")


############ UPDATE OPERATION ############

def user_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the user table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        user_name = input("Enter user_name that you intend change >> ")
        id1 = 'id'
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user_id : ", user_id)
        cursor.execute("""
            UPDATE User SET  {0} = ? WHERE {1} = ?""".format(column_name, id1), (new_value, user_id))
        conn.commit()
        print("User Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into user table", error)


def vehicles_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the vehicle information table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        plaque = input("Enter plaque that you intend change >> ")
        id1 = 'id'
        vehicle_id = cursor.execute("SELECT id FROM VehicleInformation WHERE plaque =?", (plaque,)).fetchone()[0]
        print("vehicle_id : ", vehicle_id)
        cursor.execute("""
            UPDATE VehicleInformation SET  {0} = ? WHERE {1} = ?""".format(column_name, id1), (new_value, vehicle_id))
        conn.commit()
        print("Vehicle Information Table Updated successfully")
        cursor.close()
        return True

    except sqlite3.Error as error:
        print("Failed to update data into Vehicle Information table", error)


def post_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the post table do you intend to update ? >> ")
        if column_name == 'time':
            new_value = input("Enter the new posting time and enter 1 to use the current time >> ")
            if new_value == '1':
                new_value = datetime.today().strftime("%H:%M %p")
        elif column_name == 'date':
            new_value = input("Enter the new posting date and enter 1 to use the current date >> ")
            if new_value == '1':
                today = date.today()
                new_value = today.strftime("%d/%m/%Y")
        else:
            new_value = input("Enter new value >> ")

        plaque = input("Enter the plaque of the vehicle for which you want to update the post >> ")
        id1 = 'id'
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        print("post_id : ", post_id)
        cursor.execute("""
                UPDATE Post SET  {0} = ? WHERE {1} = ?""".format(column_name, id1),
                       (new_value, post_id))
        conn.commit()
        print("Post Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into post table", error)


def comment_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the put comment table do you intend to update ? >> ")
        if column_name == 'time':
            new_value = input("Enter the new comment time and enter 1 to use the current time >> ")
            if new_value == '1':
                new_value = datetime.today().strftime("%H:%M %p")
        elif column_name == 'date':
            new_value = input("Enter the new posting date and enter 1 to use the current date >> ")
            if new_value == '1':
                today = date.today()
                new_value = today.strftime("%d/%m/%Y")
        else:
            new_value = input("Enter new value >> ")

        user_name = input("Enter the username of the person who left the comment >>  ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        date_, time_, h = input("Enter the date and time the comment was posted >> ").split()
        time_ = time_ + " " + h
        print("time entered is :", time_)
        comment_id = cursor.execute("SELECT id FROM PutComment WHERE user_id=? AND date=? AND time=?",
                                    (user_id, date_, time_)).fetchone()[0]
        id1 = 'id'
        print("comment id : ", comment_id)
        cursor.execute("""
                    UPDATE PutComment SET  {0} = ? WHERE {1} = ?""".format(column_name, id1),
                       (new_value, comment_id))
        conn.commit()
        print("Comment Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into comment table", error)


def permission_update(conn):
    cursor = conn.cursor()
    try:
        column_name = 'name'
        new_value = input("Enter new value >> ")
        name_permission = input("Enter name that you intend change >> ")
        id1 = 'id'
        per_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("id : ", per_id)
        cursor.execute("""
              UPDATE Permission SET  {0} = ? WHERE {1} = ?""".format(column_name, id1), (new_value, per_id))
        conn.commit()
        print("Permission Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into permission table", error)


def section_update(conn):
    cursor = conn.cursor()
    try:
        column_name = 'name'
        new_value = input("Enter new value >> ")
        name_section = input("Enter name that you intend change >> ")
        id1 = 'id'
        sec_id = cursor.execute("SELECT id FROM Section WHERE name=?", (name_section,)).fetchone()[0]
        print("id : ", sec_id)
        cursor.execute("""
                  UPDATE Section SET  {0} = ? WHERE {1} = ?""".format(column_name, id1), (new_value, sec_id))
        conn.commit()
        print("Section Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into section table", error)


def post_vehicle_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the post vehicle table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        plaque = input("Enter plaque that you intend change >> ")
        id1 = 'vehicle_id'
        vehicle_id = cursor.execute("SELECT id FROM VehicleInformation WHERE plaque =?", (plaque,)).fetchone()[0]
        print("vehicle_id : ", vehicle_id)
        cursor.execute("""
               UPDATE PostVehicles SET  {0} = ? WHERE {1} = ?""".format(column_name, id1),
                       (new_value, vehicle_id))
        conn.commit()
        print("Post Vehicles Table Updated successfully")
        cursor.close()
        return True

    except sqlite3.Error as error:
        print("Failed to update data into Post Vehicles table", error)


def favorite_archive_fail_update(conn, choice_update):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        plaque = input("Enter the plaque of the vehicle for which you want to update the post >> ")
        id1 = 'post_id'
        id2 = 'user_id'
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        print("post_id : ", post_id)
        user_name = input("Enter the User Name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        if choice_update == 5:
            cursor.execute("""
                      UPDATE FavoriteVehicles SET  {0} = ? WHERE {1} = ? AND {2} = ?""".format(column_name, id1, id2),
                           (new_value, post_id, user_id))
            conn.commit()
        if choice_update == 6:
            cursor.execute("""
                                  UPDATE ArchiveVehicles SET  {0} = ? WHERE {1} = ? AND {2} = ?""".format(column_name,
                                                                                                          id1, id2),
                           (new_value, post_id, user_id))
            conn.commit()
        else:
            cursor.execute("""
                              UPDATE FailVehicles SET  {0} = ? WHERE {1} = ? AND {2} = ?""".format(column_name, id1,
                                                                                                   id2),
                           (new_value, post_id, user_id))
            conn.commit()
        print("Fail or archive o favorite Vehicles Table Updated successfully")
        cursor.close()
        return True

    except sqlite3.Error as error:
        print("Failed to update data into Fail Vehicles table", error)


def user_permission_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        name_permission = input("Enter name permission that you intend change >> ")
        id1 = 'permission_id'
        per_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("id : ", per_id)
        user_name = input("Enter the User Name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        id2 = 'user_id'
        cursor.execute("""UPDATE UserPermission SET  {0} = ? WHERE {1} = ? AND {2} = ?""".format(column_name, id1, id2),
                       (new_value, per_id, user_id))
        conn.commit()
        print("User Permission Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into User Permission table", error)


def section_permission_update(conn):
    cursor = conn.cursor()
    try:
        column_name = input("Which column of the table do you intend to update ? >> ")
        new_value = input("Enter new value >> ")
        name_permission = input("Enter name permission that you intend change >> ")
        id1 = 'permission_id'
        per_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("id : ", per_id)
        name_section = input("Enter name section that you intend change >> ")
        sec_id = cursor.execute("SELECT id FROM Section WHERE name=?", (name_section,)).fetchone()[0]
        print("id : ", sec_id)
        id2 = 'section_id'
        cursor.execute(
            """UPDATE SectionPermission SET  {0} = ? WHERE {1} = ? AND {2} = ?""".format(column_name, id1, id2),
            (new_value, per_id, sec_id))
        conn.commit()
        print("Section Permission Table Updated successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to update data into Section Permission table", error)


def update_tables(conn):
    print_tables_name()
    choice_update = int(input("Which table are you going to update ?  "))
    if choice_update == 1:
        return user_update(conn)
    elif choice_update == 2:
        return vehicles_update(conn)
    elif choice_update == 3:
        return post_update(conn)
    elif choice_update == 4:
        return post_vehicle_update(conn)
    elif choice_update == 5 or choice_update == 6 or choice_update == 7:
        return favorite_archive_fail_update(conn, choice_update)
    elif choice_update == 8:
        return comment_update(conn)
    elif choice_update == 9:
        return section_update(conn)
    elif choice_update == 10:
        return permission_update(conn)
    elif choice_update == 11:
        return user_permission_update(conn)
    else:
        return section_permission_update(conn)


######### SPECIAL QUERIES #########

def print_queries():
    print("1.  Seller info Vehicle with special model and color")
    print("2.  The average price of luxury, sports and economy cars in the last three years")
    print("3.  Model, price and function of all machines with a certain price range")
    print("4.  How many of their favorite vehicles have each user failed to purchase?")
    print("5.  Name, price and ID of the seller of the cars whose manufacturer is specified")
    print("6.  Name, price and color of the vehicle in the post with the most likes and comments")
    print("7.  Models and prices of vehicles that have been manufactured for the past two years and their function is "
          "less than a certain amount.")
    print("8.  The names of all users who are older than the age of the person who sold the most expensive vehicle.")
    print("9.  Show prices and models of all motorcycles whose year is the last three years")
    print("10. Name of the user who left the most comments and the number of comments left")
    print("11. How many failure table vehicles are white ")
    print('12. Show vehicles I could not buy because of the price')
    print("13. Dealers of all vehicles whose vehicle price is higher than the price of the vehicle set by the user "
          "with a specific name.")
    print("14. Show model, price, family and contact number of the seller of equipment that has installment sales and "
          "price range less than a certain amount")
    print("15. Each user puts a few comments with a specific phrase under a particular user's favorite posts.")


def query_one(conn):
    try:
        cursor = conn.cursor()
        name = input("Enter the model >> ")
        color = input("Enter the color >> ")
        cursor.execute(
            "SELECT user.first_name,user.last_name FROM User AS user , Vehicleinformation AS v "
            "WHERE user.id = v.user_id AND v.color = ? AND v.name = ?", (color, name))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['First Name', 'Last Name'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 1 =( ", error)


def query_two(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT level , AVG(price) FROM Vehicleinformation WHERE year_construction BETWEEN 1396 AND "
            "1399 GROUP BY level")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Type', 'Avg'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 2 =( ", error)


def query_three(conn):
    try:
        cursor = conn.cursor()
        upper = int(input("Enter the upper limit of the price >> "))
        lower = int(input("Enter the lower limit of the price >> "))
        cursor.execute(
            "SELECT name,price,function FROM Vehicleinformation WHERE type = 0 AND price BETWEEN ? AND ?",
            (lower, upper))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)', 'Function (KM)'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 3 =( ", error)


def query_four(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT FR.user_id,U.first_name,U.last_name,COUNT(*) "
            "FROM User as U, FavoriteVehicles AS FR, FailVehicles AS FI WHERE FI.user_id = FR.user_id "
            "AND FR.post_id = FI.post_id AND U.id = FR.user_id AND U.id = FI.user_id GROUP BY FR.user_id")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['User ID', 'First Name', 'Last Name', 'Count'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 4 =( ", error)


def query_five(conn):
    try:
        cursor = conn.cursor()
        company = input("Enter the Company >> ")
        cursor.execute(
            "SELECT V.name,V.price,U.id FROM Vehicleinformation AS V,User AS U "
            "WHERE V.type = 0 AND V.copmany = ? AND V.user_id = U.id ", (company,))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)', 'Seller ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 5 =( ", error)


def query_six(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name,price,color FROM VehicleInformation WHERE id = "
            "(SELECT vehicle_id FROM PostVehicles WHERE post_id = (SELECT post_id FROM "
            "(SELECT post_id FROM FavoriteVehicles UNION ALL SELECT post_id FROM PutComment) "
            "GROUP BY post_id ORDER BY COUNT(*) DESC LIMIT 1))")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)', 'Color'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 6 =( ", error)


def query_seven(conn):
    try:
        cursor = conn.cursor()
        function = int(input("Enter the upper function >> "))
        cursor.execute(
            "SELECT name,price FROM Vehicleinformation WHERE year_construction BETWEEN 1397 AND 1399 AND function < ?",
            (function,))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 7 =( ", error)


def query_eight(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT first_name,last_name,user_name FROM User "
            "WHERE age > (SELECT age FROM User "
            "WHERE id = (SELECT user_id FROM Vehicleinformation ORDER BY price DESC LIMIT 1))")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['First Name', 'Last Name', 'User Name'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 8 =( ", error)


def query_nine(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name,price FROM Vehicleinformation WHERE type = 1 AND year_construction BETWEEN 1396 AND 1399")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 9 =( ", error)


def query_ten(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT u.first_name,u.last_name, count(*) as commentCount"
            " FROM PutComment AS put ,User AS u WHERE u.id = put.user_id "
            "GROUP BY put.user_id ORDER BY commentCount DESC limit 1")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['First Name', 'Last Name', 'Count'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 10 =( ", error)


def query_eleven(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM ArchiveVehicles AS A,Vehicleinformation AS V,PostVehicles AS P "
            "WHERE P.post_id = A.post_id AND P.vehicle_id = v.id AND V.color='sefid'")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Count'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 11 =( ", error)


def query_twelve(conn):
    try:
        cursor = conn.cursor()
        user_name = input("Enter the User Name >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        cursor.execute(
            "SELECT V.name,V.color,V.price FROM FailVehicles AS F,Vehicleinformation AS V,PostVehicles AS P WHERE "
            "F.description LIKE '%gheymat%' AND F.post_id = P.post_id AND P.vehicle_id = V.id AND F.user_id=?",
            (user_id,))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Color', 'Price (Millions)'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 12 =( ", error)


def query_thirteen(conn):
    try:
        cursor = conn.cursor()
        first_name, last_name, user_id = input("Enter the User info (first name space last name space user name and "
                                               "must be unique) >> ").split(" ")
        cursor.execute(
            "SELECT user_name FROM User WHERE id IN "
            "(SELECT user_id FROM Vehicleinformation WHERE price >"
            "(SELECT price FROM VehicleInformation WHERE user_id = "
            "(SELECT id FROM User WHERE first_name = ? AND last_name =? AND user_name = ?)))",
            (first_name, last_name, user_id))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['User Name'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 13 =( ", error)


def query_fourteen(conn):
    try:
        cursor = conn.cursor()
        price = int(input("Enter the upper price >> "))
        cursor.execute(
            "SELECT V.name,V.price,U.last_name,U.phone_number FROM "
            "Vehicleinformation AS V,User AS U WHERE V.user_id = U.id AND V.is_installment= true AND V.price < ?",
            (price,))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['Model', 'Price (Millions)', 'Last Name', 'Phone Number'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 7 =( ", error)


def query_fifteen(conn):
    try:
        cursor = conn.cursor()
        expression = input("Enter expression >> ")
        first_name, last_name, user_id = input("Enter the User info >> ").split(" ")
        cursor.execute(
            "SELECT first_name, last_name,number FROM User INNER JOIN"
            " (SELECT post_id,user_id,text, COUNT(*) AS number FROM PutComment WHERE post_id IN "
            "(SELECT post_id FROM FavoriteVehicles WHERE post_id = "
            "(SELECT id FROM USER WHERE first_name = ? AND last_name = ? AND user_name = ?)) "
            "GROUP BY user_id HAVING text LIKE ? ) ON user_id = id",
            (first_name, last_name, user_id, '%' + expression + '%'))
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(['First Name', 'Last Name', 'Number'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to read query 15 =( ", error)


def special_queries(conn):
    print_queries()
    choice_query = int(input("Which query do you intend to use? "))
    if choice_query == 1:
        return query_one(conn)
    elif choice_query == 2:
        return query_two(conn)
    elif choice_query == 3:
        return query_three(conn)
    elif choice_query == 4:
        return query_four(conn)
    elif choice_query == 5:
        return query_five(conn)
    elif choice_query == 6:
        return query_six(conn)
    elif choice_query == 7:
        return query_seven(conn)
    elif choice_query == 8:
        return query_eight(conn)
    elif choice_query == 9:
        return query_nine(conn)
    elif choice_query == 10:
        return query_ten(conn)
    elif choice_query == 11:
        return query_eleven(conn)
    elif choice_query == 12:
        return query_twelve(conn)
    elif choice_query == 13:
        return query_thirteen(conn)
    elif choice_query == 14:
        return query_fourteen(conn)
    else:
        return query_fifteen(conn)


######### FETCH OPERATION #########


def fetch_user(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['ID', 'First Name', 'Last Name', 'Is Deleted', 'Phone Number', 'Token', 'Role', 'Picture', 'User Name',
             'Age', 'Password', 'National Number'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch user table ", error)


def fetch_vehicles(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VehicleInformation LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['ID', 'Model', 'Color', 'Engine Volume (cc)', 'Copmany', 'Country', 'Engine Power (hp)', 'Plaque',
             'Function (KM)',
             'Is Painted', 'Level', 'State City', 'State Neighbourhood', 'Year Construction', 'Is Installment',
             'Accelleration (s)', 'Gearbox', 'Fuel Type', 'Picture', 'User ID', 'Price (Millions)', 'Type'])
        print(list_of_data)
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch vehicle information table ", error)


def fetch_post(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Post LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['ID', 'Is Deleted', 'User ID', 'Date', 'Time'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Post table ", error)


def fetch_post_vehicle(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PostVehicles LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['Post ID', 'Vehicle ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Post Vehicles table ", error)


def fetch_favorite_archive_post(conn, fetch):
    try:
        cursor = conn.cursor()
        if fetch == 5:
            cursor.execute("SELECT * FROM FavoriteVehicles LIMIT 10")
        else:
            cursor.execute("SELECT * FROM ArchiveVehicles LIMIT 10")

        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['User ID', 'Post ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch archive or favorite Vehicles table ", error)


def fetch_fail_post(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FailVehicles LIMIT 10")

        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['Description', 'User ID', 'Post ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Fail Vehicles table ", error)


def fetch_put_comment(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PutComment LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['ID', 'Time', 'Date', 'Text', 'User ID', 'Post ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Put Comment table ", error)


def fetch_section_permission_table(conn, fetch):
    try:
        cursor = conn.cursor()
        if fetch == 9:
            cursor.execute("SELECT * FROM Section LIMIT 10")
        else:
            cursor.execute("SELECT * FROM Permission LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['ID', 'Name'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Permission or Section table ", error)


def fetch_user_permission(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM UserPermission LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['User ID', 'Permission ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch User Permission table ", error)


def fetch_section_permission(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SectionPermission LIMIT 10")
        rows = cursor.fetchall()
        list_of_data = []
        for row in rows:
            list_of_data.append(list(row))
        table = PrettyTable(
            ['Section ID', 'Permission ID'])
        for rec in list_of_data:
            table.add_row(rec)
        print(table)
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to fetch Section Permission table ", error)


def fetch_tables(conn):
    print_tables_name()
    fetch_choice = int(input("Which table of contents do you want to see? "))
    if fetch_choice == 1:
        return fetch_user(conn)
    elif fetch_choice == 2:
        return fetch_vehicles(conn)
    elif fetch_choice == 3:
        return fetch_post(conn)
    elif fetch_choice == 4:
        return fetch_post_vehicle(conn)
    elif fetch_choice == 5 or fetch_choice == 6:
        return fetch_favorite_archive_post(conn, fetch_choice)
    elif fetch_choice == 7:
        return fetch_fail_post(conn)
    elif fetch_choice == 8:
        return fetch_put_comment(conn)
    elif fetch_choice == 9 or fetch_choice == 10:
        return fetch_section_permission_table(conn, fetch_choice)
    elif fetch_choice == 11:
        return fetch_user_permission(conn)
    else:
        return fetch_section_permission(conn)


######### FETCH OPERATION #########

def delete_user(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter user_name that you intend delete >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user_id : ", user_id)
        cursor.execute("""DELETE FROM User WHERE id=?""", (user_id,))
        conn.commit()
        print("User Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from user table", error)


def delete_vehicle(conn):
    cursor = conn.cursor()
    try:
        plaque = input("Enter plaque that you intend delete >> ")
        vehicle_id = cursor.execute("SELECT id FROM VehicleInformation WHERE plaque =?", (plaque,)).fetchone()[0]
        print("vehicle_id : ", vehicle_id)
        cursor.execute("""DELETE FROM VehicleInformation WHERE id=?""", (vehicle_id,))
        conn.commit()
        print("Vehicle Information Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from Vehicle Information table", error)


def delete_post(conn, delete_choice):
    cursor = conn.cursor()
    try:
        plaque = input("Enter the plaque of the vehicle for which you want to delete the post >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        print("post_id : ", post_id)
        if delete_choice == 3:
            cursor.execute("""DELETE FROM Post WHERE id=?""", (post_id,))
            conn.commit()
        else:
            cursor.execute("""DELETE FROM PostVehicles WHERE post_id =?""", (post_id,))
            conn.commit()
        print("Vehicle Information Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from Post table", error)


def delete_favorite_archive_fail_vehicle(conn, delete_choice):
    cursor = conn.cursor()
    try:
        plaque = input("Enter the plaque of the vehicle for which you want to delete the post >> ")
        post_id = cursor.execute("SELECT post_id FROM VehicleInformation,"
                                 "PostVehicles WHERE plaque =? AND id = vehicle_id", (plaque,)).fetchone()[0]
        print("post_id : ", post_id)
        user_name = input("Enter user_name that you intend delete >> ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        print("user_id : ", user_id)
        if delete_choice == 5:
            cursor.execute("""DELETE FROM FavoriteVehicles WHERE post_id =? AND user_id =?""", (post_id, user_id,))
            conn.commit()
        elif delete_choice == 6:
            cursor.execute("""DELETE FROM ArchiveVehicles WHERE post_id =? AND user_id =?""", (post_id, user_id,))
            conn.commit()
        else:
            cursor.execute("""DELETE FROM FailVehicles WHERE post_id =? AND user_id =?""", (post_id, user_id,))
            conn.commit()
        print("Archive or Fail or Favorite Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from archive or fail or favorite table", error)


def delete_comment(conn):
    cursor = conn.cursor()
    try:
        user_name = input("Enter the username of the person who left the comment >>  ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        date_, time_, h = input("Enter the date and time the comment was posted >> ").split()
        time_ = time_ + " " + h
        print("time entered is :", time_)
        comment_id = cursor.execute("SELECT id FROM PutComment WHERE user_id=? AND date=? AND time=?",
                                    (user_id, date_, time_)).fetchone()[0]
        print("comment id : ", comment_id)
        cursor.execute("""DELETE FROM PutComment WHERE id =?""", (comment_id,))
        conn.commit()
        print("Comment Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from comment table", error)


def delete_section(conn):
    cursor = conn.cursor()
    try:
        name_section = input("Enter name that you intend delete >> ")
        sec_id = cursor.execute("SELECT id FROM Section WHERE name=?", (name_section,)).fetchone()[0]
        print("Section id : ", sec_id)
        cursor.execute("""DELETE FROM Section WHERE id=?""", (sec_id,))
        conn.commit()
        print("Section Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from Section table", error)


def delete_permission(conn):
    cursor = conn.cursor()
    try:
        name_permission = input("Enter name that you intend delete >> ")
        per_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("Permission id : ", per_id)
        cursor.execute("""DELETE FROM Permission WHERE id=?""", (per_id,))
        conn.commit()
        print("Permission Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from Permission table", error)


def delete_user_permission(conn):
    cursor = conn.cursor()
    try:
        name_permission = input("Enter name permission that you intend delete >> ")
        per_id = cursor.execute("SELECT id FROM Permission WHERE name=?", (name_permission,)).fetchone()[0]
        print("Permssion id : ", per_id)
        user_name = input("Enter the username >>  ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        cursor.execute("""DELETE FROM UserPermission WHERE permission_id =? AND user_id=? """, (per_id, user_id,))
        conn.commit()
        print("User Permission Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from User Permission table", error)


def delete_section_permission(conn):
    cursor = conn.cursor()
    try:
        name_section = input("Enter name section that you intend delete >> ")
        sec_id = cursor.execute("SELECT id FROM Section WHERE name=?", (name_section,)).fetchone()[0]
        print("Section id : ", sec_id)
        user_name = input("Enter the username >>  ")
        user_id = cursor.execute("SELECT id FROM User WHERE user_name=?", (user_name,)).fetchone()[0]
        cursor.execute("""DELETE FROM SectionPermission WHERE section_id =? AND user_id =?""", (sec_id, user_id,))
        conn.commit()
        print("Section Permission Deleted successfully")
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Failed to delete data from Section Permission table", error)


def delete_tables(conn):
    print_tables_name()
    delete_choice = int(input("From which table do you intend to delete the data? "))
    if delete_choice == 1:
        return delete_user(conn)
    elif delete_choice == 2:
        return delete_vehicle(conn)
    elif delete_choice == 3 or delete_choice == 4:
        return delete_post(conn, delete_choice)
    elif delete_choice == 5 or delete_choice == 6 or delete_choice == 7:
        return delete_favorite_archive_fail_vehicle(conn, delete_choice)
    elif delete_choice == 8:
        return delete_comment(conn)
    elif delete_choice == 9:
        return delete_section(conn)
    elif delete_choice == 10:
        return delete_permission(conn)
    elif delete_choice == 11:
        return delete_user_permission(conn)
    else:
        return delete_section_permission(conn)


def main():
    database = r"vehicles.db"
    print("Welcome to the vehicle database application *_* ")
    # create a database connection
    conn = create_connection(database)
    loop = True
    while loop:
        print_menu()
        choice = int(input("Enter your choice [1-6]: "))
        with conn:
            if choice == 1:
                print("Menu 1 has been selected")
                loop = inset_to_tables(conn)
            elif choice == 2:
                print("Menu 2 has been selected")
                loop = fetch_tables(conn)
            elif choice == 3:
                print("Menu 3 has been selected")
                loop = delete_tables(conn)
            elif choice == 4:
                print("Menu 4 has been selected")
                loop = update_tables(conn)
            elif choice == 5:
                print("Menu 5 has been selected")
                loop = special_queries(conn)
            elif choice == 6:
                print("Menu 6 has been selected")
                loop = False
    conn.close()


if __name__ == '__main__':
    main()
