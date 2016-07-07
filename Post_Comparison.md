# Comparing PC, Moble and Python Post File Format

## PC (From Chrome)
```
POST http://testwww.iquicker.com.cn/iquicker_web/common/file/upload/blog HTTP/1.1
Host: testwww.iquicker.com.cn
Connection: keep-alive
Content-Length: 39897
Origin: http://testwww.iquicker.com.cn
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryTVyyhozBcJMjNOGD
Accept: */*
Referer: http://testwww.iquicker.com.cn/home/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: JSESSIONID=D95508918C02EE4DFA056993ECFAE9D2; Hm_lvt_2141421d5aca6e1e550d8cf37d85f716=1467336641,1467594925; Hm_lpvt_2141421d5aca6e1e550d8cf37d85f716=1467615069

------WebKitFormBoundaryTVyyhozBcJMjNOGD
Content-Disposition: form-data; name="file"; filename="1.png"
Content-Type: image/png

âPNG
```
## Mobile
```
POST http://testwww.iquicker.com.cn/iquicker_web/common/file/upload/blog HTTP/1.1
Content-Type: multipart/form-data; boundary=+++++
Cookie: JSESSIONID=4D115CAE21D20F11592B59F81B52D3D4; rememberMe=tQsGcx4wcOnDolqLoS7kqrZx5+TNHc/RhB3spL8J+AOEPRZ0wk8BBOryLMWxGCLiiKleN7+5Rho/XZ6OuU0bg3LHkRYqLVoEm29f5sIQxvet96v4CzeM0HjP9Fabmw+pN0AaFxuFUkvHM7+cweZrWz9OlFNdORHm+gwgYEfE9V0Rp6RUOTKfDRBE9WPd4dK9vyIu4lcjo1IZjvn7wqX7aIWHUkHU+BJuJYvpRsJxtbLt4XwTO8JnsNQZz6MB9Z4MEaVwJEbcwXoLX5fqB3/HKtOgn9y+3sVPDwMjEUnHHhLlg+d1Gi2nMWDqtzYpX95t7vObZC3uyF//Cpvdk7aRw5qte3Ct5XPiWah9uVANVNh6L38wmbVV5GwcF7zqOWNtcCn1b2iR4wEgjTonuVcHXcnSpR3LKhXZqTI63Vc+bCmGkaHpI5IYoHccYUGjYkZAFZbN3IHwgG9fGU+hst4dL5g0lFDN+cNHsLEbn+q++eHEzQhFaKyrOG0eVgd6VpEcAbOI8pmuuGkZdaRTzxHRCdmB58aGikQyXmgnEu+7SdK7hLEwlBKAJ6HQ3DafiUyF/V76D4RKeahB6lwFO+fqYbKG8g6yZiJaPYutdDFFsuCCAux8Ahh/L4xgMbfEpp3nygcjHdeNJRw4FAtAM1NDX8lx9qbLdaoBDF4UojUvDsjILu/hbRDKA0UwyVp/ojlW28M6ON8YWIC8yY/mtcGntgWtSrPGZAsCgXD6L8Gy1JfEM/JFtEyhoxWg3irTK5ZrzOhbfJ5BGh3wM8nZVPwEI09eU6gCaTA2vFGLBDuYbZk=
Transfer-Encoding: chunked
User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; 2014011 MIUI/V7.2.1.0.KHFCNDA)
Host: testwww.iquicker.com.cn
Connection: Keep-Alive
Accept-Encoding: gzip

3ff8
--+++++
Content-Disposition: form-data; name="file"; filename="image.jpg"
Content-Type: image/jpeg

âPNG
```
## My Python Simulation
```
POST http://testwww.iquicker.com.cn/iquicker_web/common/file/upload/blog HTTP/1.1
Content-Length: 433295
Accept-Encoding: gzip
Host: testwww.iquicker.com.cn
User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; 2014011 MIUI/V7.2.1.0.KHFCNDA)
Connection: close
Cookie: JSESSIONID=E37367D7FB4EEECDE932B1A7D08B2D7A; rememberMe=/26UjcvC0/BG6PGA+dgaLhDp0m2jtX55e/HDuGs+n1Yx2wBP7aQv2HsDa3gdfmrPY6/4JcysEryUMO2BMqKYCcqTweYv90vgF/ykTFK/IthMyhZ0SuSP0ceWRLnsjC7gArFAk13Y4ub26Cn97H3Ro4rkX5V3fQBYzbPVuL/PFWCkXNpmFoFP2G2gM8y5q68WES4YLUsJChGDr7k3H1sgMx4DyjurShDwEGmZ7DNJF4ICKoywEWK3uSkGEwgT36RXEzz9SUTdb939xR6kA5nVFre7K7CjJyJgoKizVi8i47uZc33ck68qxdtKRV2+ZKLvUpp7ofzoN0rJa+0cn5ZD2bOea8URtCM7232tsBCP0032yJGXzW00cpFSYxsRlZTgSnsU4e5wZwMP1h7q8cgRE4p9/vrovgmBGUNmEsXGNbJkusl4WrkaUgVO8GuqaI6Z5Blw2H3CT3TcrN0hwP3DpRoo0j78fJaAlLELXnD6A7xEhbjRonNdphPXsmavVfnuNaweoHPVKgsmTkDGH45/jxrgekZtAbRO5ul4BDMK+5di4fyeBWN7zoNhWmNjLa28fK1MX56jB0Sde1YJnDewKijnPZMs/Sti09XnF3eU4bfuJx3evIbPsLfeqzn8Vkwna1k2w+Bs9Ugo1dHg04ypVOp+LHEdegOgN6N9hIh6lbl+oK9QglCmR0bF7m4b+v1bd77EOErx4hbimek+ifS0XtH7NaJ8y22eojupnsCkbQb6A7JC2FgqcBzHHNzIqRYTkRFz/LpIQtDdlm90j/E0bg01pCHlM3uMYdb1GqAcHQU=
Content-Type: multipart/form-data; boundary=+++++

3ff8
--+++++
Content-Disposition: form-data; name="file"; filename="Mapping.jpg"
Content-Type: image/jpeg

âPNG
```
