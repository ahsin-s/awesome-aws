# Find and upload all .html, .css, and .js files preserving directory structure
find . -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) | while read -r file; do
  # Remove leading ./ to preserve relative paths
  s3_key="${file#./}"
  bucket_name=www.$DOMAIN_NAME
  upload_dest=s3://$bucket_name/$s3_key

  # Upload to S3
  aws s3 cp "$file" "$upload_dest" --only-show-errors
  echo "Uploaded: $file -> $upload_dest"
done