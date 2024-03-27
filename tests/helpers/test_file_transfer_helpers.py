import unittest
from unittest.mock import MagicMock, patch
from helpers.file_transfer_helpers import PlexHelperFunctions
import random
import string

class TestFileTransferHelpers(unittest.TestCase):
    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.load')
    def test_get_conf_val(self, mock_json_load, mock_open):
        mock_config = {
            "home_folder": {
                "Folder": "/home/manny/plex_transfer"
            }
        }
        mock_json_load.return_value = mock_config

        obj_plex = PlexHelperFunctions()
        result = obj_plex.get_conf_val("home_folder")

        self.assertEqual(result, "/home/manny/plex_transfer")

    @patch.object(PlexHelperFunctions, 'get_conf_val')
    @patch('glob.glob')
    def test_get_files(self, mock_glob, mock_get_conf_val):
        # Mock the return value of get_conf_val
        mock_base_folder_name = "/media/manny/Backups/MASM"
        mock_get_conf_val.return_value = mock_base_folder_name

        # Mock the return value of glob.glob
        mock_file_list = ["/media/manny/Backups/MASM/BOUND TO LEASE 10.mp4", "/media/manny/Backups/MASM/BOUND TO LEASE 05.mp4"]
        mock_glob.return_value = mock_file_list

        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()
        
        # Call the get_files method
        result = obj_plex.get_files()

        # Assert that get_conf_val was called with "base_folder"
        mock_get_conf_val.assert_called_once_with("base_folder")
        # Assert that glob.glob was called with the correct path
        mock_glob.assert_called_once_with(f"{mock_base_folder_name}/*")
        # Assert that the result matches the expected file list
        self.assertEqual(result, mock_file_list)

    @patch.object(PlexHelperFunctions, 'get_conf_val')
    @patch('glob.glob')
    @patch('os.path.getctime')
    def test_get_last_file(self, mock_getctime, mock_glob, mock_get_conf_val):
        # Mock the return value of get_conf_val
        mock_base_folder_name = "/media/manny/Backups/MASM"
        mock_get_conf_val.return_value = mock_base_folder_name

        # Mock the return value of glob.glob
        mock_file_list = ["/media/manny/Backups/MASM/BOUND TO LEASE 10.mp4", "/media/manny/Backups/MASM/BOUND TO LEASE 05.mp4"]
        mock_glob.return_value = mock_file_list

        # Mock the return value of os.path.getctime
        mock_getctime.side_effect = [100, 200]  # Mocking creation times for files

        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()
        
        # Call the get_last_file method
        result = obj_plex.get_last_file()

        # Assert that get_conf_val was called with "base_folder"
        mock_get_conf_val.assert_called_once_with("base_folder")
        # Assert that glob.glob was called with the correct path
        mock_glob.assert_called_once_with(f"{mock_base_folder_name}/*")
        # Assert that os.path.getctime was called for each file in the file list
        mock_getctime.assert_any_call("/media/manny/Backups/MASM/BOUND TO LEASE 10.mp4")
        mock_getctime.assert_any_call("/media/manny/Backups/MASM/BOUND TO LEASE 05.mp4")
        # Assert that the result matches the expected latest file
        self.assertEqual(result, "/media/manny/Backups/MASM/BOUND TO LEASE 05.mp4")

    @patch('random.choice')
    def test_generate_batch_ID(self, mock_choice):
        # Mock random.choice to return 'a' for all characters
        mock_choice.side_effect = lambda x: 'a'

        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()

        # Call the generate_batch_ID method with length 5
        result = obj_plex.generate_batch_ID(5)

        # Assert that random.choice was called with the correct argument
        mock_choice.assert_called_with(string.ascii_lowercase + string.digits)
        # Assert that the result matches the expected value ('aaaaa')
        self.assertEqual(result, 'aaaaa')

    def test_remove_special_chars_from_file_name(self):
        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()

        # Define input file names with special characters
        input_file_names = [
            "file!name$with%special&characters",
            "another_file:name;with?special@characters",
            "file|name}with~special{chars",
            "file`name`with`backticks"
        ]

        # Define expected file names without special characters
        expected_file_names = [
            "filenamewithspecialcharacters",
            "anotherfilenamewithspecialcharacters",
            "filenamewithspecialchars",
            "filenamewithbackticks"
        ]

        # Iterate through input file names and expected file names
        for input_name, expected_name in zip(input_file_names, expected_file_names):
            # Call the remove_special_chars_from_file_name method
            result = obj_plex.remove_special_chars_from_file_name(input_name)
            # Assert that the result matches the expected file name
            self.assertEqual(result, expected_name)


    def test_strip_folder_name(self):
        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()

        # Define input complete paths
        input_paths = [
            "/path/to/folder/file.txt",
            "/another/path/to/another/folder/",
            "single_file.txt",
            "/",
            ""
        ]

        # Define expected folder names
        expected_names = [
            "file.txt",
            "",
            "single_file.txt",
            "",
            ""
        ]

        # Iterate through input paths and expected names
        for input_path, expected_name in zip(input_paths, expected_names):
            # Call the strip_folder_name method
            result = obj_plex.strip_folder_name(input_path)
            # Assert that the result matches the expected folder name
            self.assertEqual(result, expected_name)



    @patch('os.rename')
    @patch.object(PlexHelperFunctions, 'remove_special_chars_from_file_name')
    @patch.object(PlexHelperFunctions, 'get_conf_val')
    def test_remove_special_characters_from_filename(self, mock_get_conf_val, mock_remove_special_chars_from_file_name, mock_rename):
        # Mock the return value of get_conf_val
        mock_base_folder_name = "/media/manny/Backups/MASM"
        mock_get_conf_val.return_value = mock_base_folder_name

        # Mock the return value of remove_special_chars_from_file_name
        mock_remove_special_chars_from_file_name.return_value = "BOUND_TO_LEASE_10.mp4"

        # Create an instance of YourClass
        obj_plex = PlexHelperFunctions()

        # Define a list of mock file paths
        mock_file_list = [
            "/media/manny/Backups/MASM/BOUND#TO#LEASE#10.mp4"
                ]

        # Call the remove_special_characters_from_filename method
        obj_plex.remove_special_characters_from_filename(mock_file_list)


        # Assert that remove_special_chars_from_file_name was called for each file
        mock_remove_special_chars_from_file_name.assert_any_call("BOUND#TO#LEASE#10.mp4")
        
        

        # Assert that os.rename was called with the correct arguments
        mock_rename.assert_any_call("/media/manny/Backups/MASM/BOUND#TO#LEASE#10.mp4", "/media/manny/Backups/MASM/BOUND_TO_LEASE_10.mp4")
        


if __name__ == '__main__':
    unittest.main()