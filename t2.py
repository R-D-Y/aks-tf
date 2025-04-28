cd /opt/apps

for file in bosh credhub fly kubelogin om pivnet uaac yq; do
    if [ -e "newbin/$file" ]; then
        if [ -e "bin/$file" ]; then
            cp newbin/$file bin/$file
            echo "Mis à jour : $file"
        else
            cp -p newbin/$file bin/
            echo "Ajouté : $file"
        fi
    else
        echo "ATTENTION : $file n'existe pas dans newbin/"
    fi
done