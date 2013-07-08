from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.utils import createContentInContainer
from zope.annotation.interfaces import IAnnotations as IStorage  # Avoid
                                # confusion with annotation content type


class ImageArtifactEditMetadata():
    """
    Browser page
    """

    def __call__(self):
        """
        Set metadata; redirect to context
        """
        contributor = self.request.form.get('contributor').split('\r\n')
        self.context.contributors = contributor

        coverage = self.request.form.get('coverage')
        self.context.coverage = coverage

        creator = self.request.form.get('creator').split('\r\n')
        self.context.creators = creator

        description = self.request.form.get('description')
        self.context.description = description

        identifier = self.request.form.get('identifier')
        self.context.identifier = identifier

        publisher = self.request.form.get('publisher')
        self.context.publisher = publisher

        relation = self.request.form.get('relation')
        self.context.relation = relation

        rights = self.request.form.get('rights')
        self.context.rights = rights

        source = self.request.form.get('source')
        self.context.source = source

        subject = self.request.form.get('subject')
        self.context.subject = subject

        self.context.reindexObject()

        return self.request.response.redirect(self.context.absolute_url())


class ImageArtifactEditTags():
    """
    Browser page
    """

    def __call__(self):
        """
        Set tags; redirect to context
        """
        tags = self.request.form.get('tags').split('\r\n')
        self.context.setSubject(tags)
        self.context.reindexObject()
        return self.request.response.redirect(self.context.absolute_url())


class ImageArtifactView():
    """
    Browser page
    """

    image_artifact_view = ViewPageTemplateFile('image_artifact.pt')

    def __call__(self):
        """
        Return the view template; handle form posts
        """
        add_another_question = False
        if self.request.method == 'POST':
            questions = []
            items = self.request.form.items()  # XXX Why not use .get()?
            for item, text in items:  # Add another question?
                if item != 'new-question':  # No
                    questions.append((item, text))
                else:  # Yes
                    add_another_question = True
            annotation = createContentInContainer(self.context, 'annotation')
            for uid, text in questions:  # Process questions
                if text is not '':
                    question = uuidToObject(uid)
                    question = question.Title()
                    title = "Response to %s"
                    response = createContentInContainer(
                        annotation, 'response', title=title % question)
                    storage = IStorage(response)
                    storage[uid] = question
                    response.description = text
            if add_another_question:
                portal = self.context.portal_url()
                self.request.response.redirect("%s/++add++question" % portal)
        return self.image_artifact_view()

    def get_questions(self):
        """
        Return content items of type "question" from the catalog
        """
        return self.context.portal_catalog(
            portal_type="question", sort_on="id", sort_order="ascending")

    def get_contributor(self):
        """
        Return contributor field as a string separated by newlines
        """
        return '\n'.join(self.context.Contributors())

    def get_creator(self):
        """
        Return creator field as a string separated by newlines
        """
        return '\n'.join(self.context.creators)

    def get_tags(self):
        """
        Return tags as a string separated by newlines
        """
        return '\n'.join(self.context.Subject())
