# Deploy no Streamlit

O app publicado depende de segredos configurados no painel do Streamlit Cloud.

## O que fazer

1. Abra o app no painel do Streamlit Cloud.
2. Entre em Manage app.
3. Abra Settings.
4. Abra Secrets.
5. Cole o conteudo do arquivo local .streamlit/secrets.toml.
6. Salve os secrets e redeploy a aplicacao.

## Template seguro

Use o arquivo .streamlit/secrets.example.toml como modelo estrutural.

## Observacao

Nao publique o arquivo real .streamlit/secrets.toml no Git. Ele contem credenciais de acesso.