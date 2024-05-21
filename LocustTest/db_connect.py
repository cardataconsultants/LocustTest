import os
import subprocess
from dotenv import load_dotenv
load_dotenv()



class DB_Connect():
    host = os.environ['host']
    port = os.environ['port']
    db_user = os.environ['db_user']
    db_password = os.environ['db_password']

    @classmethod
    def execute_query(cls, data_base):
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = 'queries.sql'
        abs_file_path = os.path.join(script_dir, rel_path)
        connect = "mariadb --host " + cls.host + " --port " + cls.port + " --user " + cls.db_user + " --password=" + cls.db_password + " " + data_base + " < " + abs_file_path
        # subprocess.run("echo $SHELL", shell=True, executable='usr/bin/zsh', check=True)
        result = subprocess.run([connect], shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout != "":
            new_result = result.stdout.split("\n")
            new_result.pop(0)
            new_result.pop()
            return new_result
        elif result.returncode == 0:
            assert True
        else:
            assert False, "Error! - " + result.stderr

    @classmethod
    def test_query(cls):
        DB_Connect.write_query(
            '"SELECT CONCAT_WS(\'|\',user_id, username, first_name, last_name) FROM AP_User WHERE username=\'qadriver\';"')
        response = (DB_Connect.execute_query("cd_master"))
        user_info = response[0].split("|")
        print(user_info)

    @classmethod
    def write_query(cls, query):
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = 'queries.sql'
        abs_file_path = os.path.join(script_dir, rel_path)
        result = subprocess.run("echo " + query + " > " + abs_file_path, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            assert False, "Error! - " + result.stderr

    @classmethod
    def db_get_user(cls, attribute, attribute_name):
        cls.write_query(
            '"SELECT CONCAT_WS(\'|\',user_id, username, first_name, last_name, company_id) FROM AP_User WHERE ' + attribute + '=\'' + attribute_name + '\';"')
        response = (cls.execute_query("cd_master"))
        if response is not None:
            user_info = response[0].split("|")
        else:
            user_info = None
        return user_info

    @classmethod
    def db_change_email(cls, email_address, username):
        query = '"UPDATE AP_User SET email = \'' + email_address + '\' WHERE username=\'' + username + '\';"'
        cls.write_query(query)
        response = (cls.execute_query("cd_master"))

    @classmethod
    # add lowercase
    def db_get_non_existent_users(cls, list_of_usernames):
        list_of_non_existent = []
        query = '"SELECT username FROM AP_User WHERE username in ' + str(list_of_usernames) + ';"'
        query = query.replace("[", "(")
        query = query.replace("]", ")")
        cls.write_query(query)
        list_of_existing_users = (cls.execute_query("cd_master"))
        if list_of_existing_users is None:
            return list_of_usernames
        else:
            for i in list_of_usernames:
                lower_i = i.lower()
                if lower_i not in list_of_existing_users:
                    list_of_non_existent.append(i)
        return list_of_non_existent

    @classmethod
    def db_get_company_stops(cls, company_id):
        query = '"SELECT company_stop_id from MI_Company_Saved_Stop WHERE company_id=' + company_id + ' and reporting_center = 1 LIMIT 1;"'
        cls.write_query(query)
        company_stop_id = cls.execute_query("cd_cardata")
        return company_stop_id

    @classmethod
    def db_set_password(cls, username):
        cls.write_query(
            '"UPDATE AP_User a1 SET password = (SELECT password from AP_User WHERE username = \'qadriver\') WHERE a1.username = \'' + username + '\';"')
        cls.execute_query("cd_master")

    @classmethod
    def get_client_id(cls, name):
        cls.write_query(
            '"SELECT CONCAT_WS(\'|\',id, name, secret) FROM oauth_clients WHERE name =\'' + name + '\';"')
        response = (cls.execute_query("cd_master"))
        user_info = response[0].split("|")
        return user_info

    @classmethod
    def get_company_id_for_test_users(cls, favr=True, country="US", sso=False, mileage_auto_classify=False):
        if favr == True:
            company = "cpm =0 AND driver_country=\'" + country + "\'"
        else:
            company = "cpm =1 AND driver_country=\'" + country + "\' and company_id !=32"
        cls.write_query(
            '"SELECT company_id FROM AP_Company WHERE ' + company + ' AND direct_pay_date != 0 AND company_id != 13 AND mileage_entry = \'tracking\' AND status_id = 1 LIMIT 1;"')
        response = (cls.execute_query("cd_master"))
        user_info = response[0]
        return user_info

    @classmethod
    def get_company_id(cls, username):
        query = '"SELECT company_id from AP_User WHERE username=\'' + username + '\';"'
        cls.write_query(query)
        response = (cls.execute_query("cd_master"))
        company_id = response[0]
        return company_id
