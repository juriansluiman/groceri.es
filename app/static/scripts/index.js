class Entity {
    _resource = '';

    constructor(resource) {
        this._resource = resource
    }

    async update (data) {
        let response = await fetch(this._resource, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            console.debug(await response.text())
            throw new Error(`Server response ${response.status}: `)
        } else if (response.status == 204) {
            console.debug('Response success, no content')
            return true
        } else {
            let json = await response.json()
            console.debug('Response success, body content: ', json)
            return json
        }
    }
}

class Recipe extends Entity {
    _rating = null;

    set rating(value) {
        this._rating = value
        this.update()
    }

    update() {
        console.debug('Update rating to ' + this._rating)
        super.update({rating: this._rating})
    }
}

class Profile extends Entity {
    _username = null;
    _email = null;
    _password = null;

    set username(value) {
        this._username = value
    }

    set email(value) {
        this._email = value
    }

    set password(value) {
        this._password = value
    }

    update() {
        super.update({
            name: this._name,
            email: this._email,
            password: this._password
        })
    }
}

export {Recipe, Profile};