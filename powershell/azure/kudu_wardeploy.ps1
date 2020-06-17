# Error Response
curl -X POST -u '<user>:<password>' <sitename> "--data-binary" "@<warpath>";

# Response header
curl -S -D - -X POST -u '<user>:<password>' <sitename> "--data-binary" "@<warpath>" -o NUL;