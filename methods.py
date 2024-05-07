from googleapiclient.http import MediaIoBaseDownload
from connection import service

# function to upload file to google drive folder if folder name is provided
def upload(filename, folder_id=None):
  """Uploads a file to a folder in Google Drive.

  Args:
    service: The Drive API service object.
    filename: The path to the file to upload.
    folder_id: The ID of the folder to upload the file to.

  Returns:
    The uploaded file metadata if successful, otherwise None.
  """
  file_metadata = {'name': filename}
  if folder_id:
    file_metadata['parents'] = [folder_id]
  media_body = filename
  try:
    file = service.files().create(
        body=file_metadata,
        media_body=media_body,
        fields='id'  # Only fetch the ID for efficiency
    ).execute()

    print(f"File uploaded successfully. ID: {file.get('id')}")
    return file
  except Exception as error:
    print(f"An error occurred: {error}")
    return None

    # Example usage
    # filename = 'sample.txt'
    # folder_id = '1oBflatbRWZOTOLpwKzLpByfBhmrMGqhg'  # Replace with the actual folder ID
    # uploaded_file = upload_file_to_folder(filename, folder_id)


# function to list files in google drive
def list_files(query=None):
  """Lists files in Google Drive.

  Args:
    service: The Drive API service object.
    query: Optional query string to filter the files.

  Returns:
    List of file metadata if successful, otherwise None.
  """
  try:
    results = service.files().list(q=query).execute()
    return results.get('files', [])
  except Exception as error:
    print(f"An error occurred: {error}")
    return None
  
    # Example usage
    # files = list_files()
    # if files:
    #   for file in files:
    #     print(f"Found file: {file['name']} ({file['id']})")
    # else:
    #   print("No files found.")


def download_file(file_id, destination_path):
    """Downloads a file from Google Drive.

    Args:
        file_id: The ID of the file to download.
        destination_path: The path to save the downloaded file.
    """
    try:
        request = service.files().get_media(fileId=file_id)
        fh = open("downloads/"+destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
                status, done = downloader.next_chunk()
                print(f"Downloaded {int(status.progress() * 100)}%.")
    except Exception as error:
        print(f"An error occurred: {error}")

    # Example usage
    # file_id = '19FtAHasQ4YaYBUdB1vuzFMh9J1KeoWoF'  # Replace with the actual file ID
    # destination_path = 'downloaded_file.txt'
    # download_file( file_id, destination_path)

# function to delete file from google drive
def delete_file(file_id):
  """Deletes a file from Google Drive.

  Args:
    service: The Drive API service object.
    file_id: The ID of the file to delete.
  """
  try:
    service.files().delete(fileId=file_id).execute()
    print(f"File with ID {file_id} deleted successfully.")
  except Exception as error:
    print(f"An error occurred: {error}")

    # Example usage
    # file_id = '1oBflatbRWZOTOLpwKzLpByfBhmrMGqhg'  # Replace with the actual file ID
    # delete_file(file_id)

# function to create folder in google drive
def create_folder(folder_name):
  """Creates a folder in Google Drive.

  Args:
    service: The Drive API service object.
    folder_name: The name of the folder to create.

  Returns:
    The created folder metadata if successful, otherwise None.
  """
  file_metadata = {
      'name': folder_name,
      'mimeType': 'application/vnd.google-apps.folder'
  }
  try:
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"Folder created successfully. ID: {folder.get('id')}")
    return folder
  except Exception as error:
    print(f"An error occurred: {error}")
    return None

    # Example usage
    # folder_name = 'My Folder'
    # created_folder = create_folder(folder_name)

# function to move file to folder in google drive
def move_file(file_id, folder_id):
  """Moves a file to a folder in Google Drive.

  Args:
    service: The Drive API service object.
    file_id: The ID of the file to move.
    folder_id: The ID of the folder to move the file to.
  """
  try:
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = service.files().update(fileId=file_id,
                                  addParents=folder_id,
                                  removeParents=previous_parents,
                                  fields='id, parents').execute()
    print(f"File with ID {file_id} moved successfully to folder with ID {folder_id}")
  except Exception as error:
    print(f"An error occurred: {error}")

    # Example usage
    # file_id = '1oBflatbRWZOTOLpwKzLpByfBhmrMGqhg'  # Replace with the actual file ID
    # folder_id = '1oBflatbRWZOTOLpwKzLpByfBhmrMGqhg'  # Replace with the actual folder ID
    # move_file(file_id, folder_id)
    