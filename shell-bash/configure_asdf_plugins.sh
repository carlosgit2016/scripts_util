source ~/.zshrc
# ASDF PLUGINS
## awscli
asdf plugin add awscli
asdf install awscli latest
asdf global awscli latest
aws --help
## saml2aws
asdf plugin-add saml2aws https://github.com/elementalvoid/asdf-saml2aws.git
asdf install saml2aws 2.36.0
asdf global saml2aws 2.36.0