from decouple import config

def message_email(msg_uuid):
    return f"""
          <table border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td>
                <p>Hi there,</p>
                <p>You've received a new password protected message!</p>
                <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                  <tbody>
                    <tr>
                      <td align="left">
                        <table border="0" cellpadding="0" cellspacing="0">
                          <tbody>
                            <tr>
                              <td> <a href="{config('APP_URL')}" target="_blank">Open</a> </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p>Message Unique Identifier: <br />{msg_uuid}</p>
                <p>The creator of the message should've sent you the password via another secure channel.</p>
              </td>
            </tr>
          </table>
    """


def activation_email(account_uuid):
    return f"""
      <table border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <p>Hi there,</p>
            <p>Thanks for registering!</p>
            <table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
              <tbody>
                <tr>
                  <td align="left">
                    <table border="0" cellpadding="0" cellspacing="0">
                      <tbody>
                        <tr>
                          <td> <a href="{config('API_URL')}/api/activate/{account_uuid}" target="_blank">Activate Account</a> </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </table>
    """