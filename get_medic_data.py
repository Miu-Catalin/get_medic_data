import click

@click.command()
@click.option('--count', default=0, help="numarul de iteratii")
@click.option('--email', prompt='adresa de email', help='adresa de email folosita pentru autentificare')
@click.password_option(confirmation_prompt=False)
def main(count, email, password):
    # autenficare in api
    # get lista cuim
    # for each get data daca nu are limita
    # write json file
    for x in range(count):
        click.echo(f'Hello {email} with {password}')

if __name__ == '__main__':
    main()
