import CryptoJS from 'crypto-js'

// 密钥和 IV 必须是 16 字节（128 位）
const SECRET_KEY = CryptoJS.enc.Utf8.parse('1234567890123456')
const IV = CryptoJS.enc.Utf8.parse('6543210987654321')

export function encrypt(text) {
  const encrypted = CryptoJS.AES.encrypt(text, SECRET_KEY, {
    iv: IV,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  })
  return encrypted.toString() // 返回 Base64 字符串
}

export function decrypt(ciphertext) {
  try {
    const decrypted = CryptoJS.AES.decrypt(ciphertext, SECRET_KEY, {
      iv: IV,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    return decrypted.toString(CryptoJS.enc.Utf8)
  } catch (e) {
    console.error('解密失败:', e)
    return ''
  }
}
