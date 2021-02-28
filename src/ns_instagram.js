const Instagram = require('instagram-web-api')
const FileCookieStore = require('tough-cookie-filestore2')
const useragentFromSeed = require('useragent-from-seed')

const argv = process.argv.slice(2)

const username = argv[0]
const password = argv[1]
const photo = argv[2]
const caption = argv[3]

const cookieStore = new FileCookieStore('./cookies.json')
const client = new Instagram({username: username, password: password, cookieStore})

;(async () => {
	await client.login()
	console.log(useragentFromSeed('newspaper_snippets'))
	await client.uploadPhoto({ photo, caption: caption, post: 'feed' })
})()
