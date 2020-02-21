# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 20:27:08 2020

@author: ПК
"""


class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        attrs = []

        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + "\n" + internal + ending + "\n"  # поставил перенос
        else:
            if self.is_single:
                return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text)

    def __iadd__(self, other):
        self.children.append(other)
        return self


class HTML:

    def __init__(self, output=None, **kwargs):  # у HTML тоже бывают атрибуты
        self.tag = "html"
        self.output = output
        self.attributes = {}
        self.children = []

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):

        if self.output:
            f = open(self.output, "w")
            f.write(str(self))
            f.close()
        else:
            print(self)

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        res = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
        for child in self.children:
            res += "\n" + str(child)

        res += "\n" + "</%s>" % self.tag
        return res

    def __iadd__(self, other):
        self.children.append(other)
        return self


class TopLevelTag:
    def __init__(self, tag, klass=None, **kwargs):  # у body тоже бывают атрибуты
        self.tag = tag
        # self.text = ""
        self.attributes = {}
        # self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        attrs = []

        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + "\n" + internal + ending
        else:
            return "<{tag} {attrs}>\n</{tag}>".format(
                tag=self.tag, attrs=attrs)

    def __iadd__(self, other):
        self.children.append(other)
        return self


with HTML(output=None) as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title

        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body
