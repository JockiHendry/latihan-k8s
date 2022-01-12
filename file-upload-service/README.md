# file-upload-service

![file-upload-service](https://github.com/JockiHendry/latihan-k8s/actions/workflows/file-upload-service.yaml/badge.svg)

This service handles tasks related to the files uploaded by user.  

## Upload

Endpoints:
* `POST https://files.latihan.jocki.me/upload`
* `POST https://files.latihan.jocki.me/<folder>/upload`

Request:
* `folder` is an optional string to represent the folder to store the file.  Use this to group files based on their purposes, for example, `logo`, `attachments`, etc.
* The content of the file in multipart/form-data.  It must have a block named as `file` that contains a `filename`.
* This endpoint can only be called by authorized user.

Response:
* A JSON that has `filename` to represent the saved filename (excluding its folder).  Store this `filename` to database and/or returned it to frontend.
* A 200x200 thumbnail for `filename` is created in `thumbnail` sub-folder relative to the specified `<folder>` in URL.  The thumbnail filename is also `filename`.  
  The thumbnail preserves image ratio so that it is not always exactly 200x200 (but one of its dimension will be 200) so styling like `object-fit` may be required when
  displaying multiple thumbnails with different dimension.
  
Example:

```
curl -F "file=@product1.png;filename=test.png;type=image/png" -X POST https://files.latihan.jocki.me/logo/upload
```

The response is a JSON that looks like:

```json
{
  "filename": "2ab02505-9f44-42f6-bea2-154551de9a3d-test.png"
}
```

## Download

Endpoint:
* `GET https://files.latihan.jocki.me/<folder>/<filename>` to retrieve the file.
* `GET https://files.latihan.jocki.me/<folder>/thumbnail/<filename>` to retrieve the thumbnail for the file is it is an image file.

Request:
* Frontend must already know what is the `<folder>`.  Usually this is hardcoded in the code itself.  For example, in item catalog pages, `itemImage` can be chosen 
  as `<folder>` value. `<folder>` is optional, when omitted, files will be stored flattened in 
  root directory.  While ext4 file system can support up to 4 billion files in a folder, but performance usually degrade as number of files increases.
* `<filename>` is the filename returned by the upload operation.

Example:

To retrieve a file:

```
curl https://files.latihan.jocki.me/logo/2ab02505-9f44-42f6-bea2-154551de9a3d-test.png
```

When displaying a lot of images in a single page, use the thumbnail URL for better performance (because thumbnail is smaller than the actual file):

```
curl https://files.latihan.jocki.me/logo/thumbnail/2ab02505-9f44-42f6-bea2-154551de9a3d-test.png
```
