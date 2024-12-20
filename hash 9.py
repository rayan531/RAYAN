import os
import imagehash
from PIL import Image

def compare_images(folder_path, hash_function=imagehash.phash, similarity_threshold=5):
    
    
    print(f"Scanning folder: {folder_path}")

   
    image_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            image_files.append(file_path)

   
    image_hashes = {}
    for file_path in image_files:
        try:
            with Image.open(file_path) as img:
                img_hash = hash_function(img)
                image_hashes[file_path] = img_hash
                print(f"Processed: {file_path} - Hash: {img_hash}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    
    duplicates = []
    image_list = list(image_hashes.items())
    for i in range(len(image_list)):
        for j in range(i + 1, len(image_list)):
            file1, hash1 = image_list[i]
            file2, hash2 = image_list[j]
            hash_difference = hash1 - hash2

            
            if hash_difference <= similarity_threshold:
                duplicates.append((file1, file2, hash_difference))
                print(f"Duplicate Found:")
                print(f"  Image 1: {file1}")
                print(f"  Image 2: {file2}")
                print(f"  Hash Difference: {hash_difference}")

    
    if duplicates:
        print("\nSummary of Duplicates:")
        for img1, img2, diff in duplicates:
            print(f"  {img1} and {img2} (Difference: {diff})")
    else:
        print("\nNo duplicate images found.")

if __name__ == "__main__":
  
    folder_path = input("Enter the folder path containing the images: ").strip()
    if os.path.isdir(folder_path):
        compare_images(folder_path)
    else:
        print("Invalid folder path. Please try again.")
