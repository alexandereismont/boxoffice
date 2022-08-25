from typing import List
import streamlit as st
import asyncio
import extra_streamlit_components as stx
from keycloak import KeycloakOpenID
import jwt
from cookie_manager import get_manager

cookie_manager = get_manager()


keycloak_openid = KeycloakOpenID(server_url="http://localhost:8180/auth/",
                    client_id="BoxofficeStreamlit",
                    realm_name="Base",
                    client_secret_key="833f7bfe-baaa-435d-bcd2-fe748c40b68f")


def check_if_authenticated() -> bool:
  print(f"cookie_manager: {cookie_manager}")
  cookie: str = cookie_manager.get("boxoffice_streamlit_app_access_token")
  print(f"cookie in check_if_authenticated {cookie}")
  if cookie is None:
    try:
      code = st.experimental_get_query_params()['code'][0]
      print(f"code: {code}")
    except:
      return False
    else:
      if cookie is None:
        token = asyncio.run(write_access_token(client=keycloak_openid, redirect_uri="http://localhost:8501", code=code))
        cookie_manager.set("boxoffice_streamlit_app_access_token", token['access_token'], key="boxoffice_streamlit_app_access_token")
        cookie_manager.set("boxoffice_streamlit_app_refresh_token", token['refresh_token'], key="boxoffice_streamlit_app_refresh_token")
        st.session_state['authenticated'] = True
        st.experimental_set_query_params()
  else:
    st.session_state['authenticated'] = True
  return True


async def write_access_token(client: KeycloakOpenID,
                             redirect_uri: str,
                             code: str):
  token = client.token(code=code, redirect_uri=redirect_uri, grant_type="authorization_code")
  return token


def write_login_url():
  auth_url = keycloak_openid.auth_url(
    redirect_uri="http://localhost:8501",
    scope="profile",
    state="password")
  st.write(f'''<h1>
                Please login using this <a target="_self"
                href="{auth_url}">url</a></h1>''',
                    unsafe_allow_html=True)


def write_userinfo(cookie: str):
  try:
    userinfo = keycloak_openid.userinfo(cookie)
    st.header(f"Hi {userinfo['preferred_username']}. You are logged in 😃")
  except:
    refresh_token = cookie_manager.get("boxoffice_streamlit_app_refresh_token")
    access_token = keycloak_openid.refresh_token(refresh_token=refresh_token)
    cookie_manager.set("boxoffice_streamlit_app_access_token", access_token['access_token'], key="boxoffice_streamlit_app_access_token")
    
    userinfo = keycloak_openid.userinfo(access_token['access_token'])
    st.header(f"Hi {userinfo['preferred_username']}. You are logged in 😃")


def get_user_roles(token) -> List[str]:
  decoded = jwt.decode(token, options={"verify_signature": False})
  return decoded['resource_access']['BoxofficeStreamlit']['roles']