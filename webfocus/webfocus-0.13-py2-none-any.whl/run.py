#!/usr/bin/env python
#-*-coding:utf-8-*- 
import click
import webfocus

version = "0.13"
program_name = "webfocus"

@click.group()
@click.version_option(version=version,prog_name=program_name)
@click.pass_context
def public(context):
    """webfocus system.simple web content extractor

    Powered by qiulimao@2017.03
    """
    return context

@public.command()
@click.option("-u","--url",prompt="INPUT TARGET URL",type=str,help=u"the target url")
@click.option("-n","--shownoise",is_flag=True,default=False,type=bool,help=u"仅输出噪声，默认为False")
@click.option("-t",'--textonly',is_flag=True,default=False,type=bool,help=u"输出不带标签的正文，默认为False")
@click.pass_context
def decision(context,url,shownoise,textonly):
    """
        [beta] use decision tree to extract the content
    """
    from extractor import extract_from_url as E
    click.echo("----------- extracting --------------------")
    info,noise = E(url,textonly)
    click.echo("/*************************\n****** the content is ******\n/*************************")
    
    if shownoise:
        click.echo(noise)
    else:
        click.echo(info)


@public.command()
@click.option("-u","--url",prompt="INPUT TARGET URL",type=str,help=u"the target url")
@click.option("-t",'--textonly',is_flag=True,default=False,type=bool,help=u"输出不带标签的正文，默认为False")
@click.pass_context
def bayes(context,url,textonly):
    """
        给定url提取相应的正文
    """
    from bayes import extract_from_url as BE
    click.echo("----------- extracting --------------------")
    info = BE(url,textonly)
    click.echo("/*************************\n****** the content is ******\n/*************************")
    
    click.echo(info)


def main():
    """
        主程序运行
    """
    public()

if __name__ == "__main__":
    """
        脚本直接运行
    """
    public()

